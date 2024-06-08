from django.contrib.auth import get_user_model
from rest_framework import permissions, viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from slugify import slugify

from post.models import Post, Comment, Category, Tag
from services import services, redis_services
from . import serializers
from .permissions import IsOwnerOrAdminUserOrReadOnly, IsAdminOrReadOnly, IsOwnerOrReadOnly


class UserViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """
    Набор представлений для модели User
    """

    def get_queryset(self):
        if self.action == 'list':
            return services.all_objects(get_user_model().objects)
        return services.all_objects(get_user_model().objects,
                                    prefetch_related=('blog_posts', 'following', 'comments'))

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.UserListSerializer
        return serializers.UserDetailSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = (IsAuthenticated,)
        else:
            permission_classes = (IsOwnerOrReadOnly,)
        return [permission() for permission in permission_classes]


# class UserList(generics.ListAPIView):
#     """Отображение списка пользователей"""
#
#     queryset = services.all_objects(get_user_model().objects)
#     serializer_class = serializers.UserListSerializer
#     # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#
#
# class UserDetail(generics.RetrieveUpdateDestroyAPIView):
#     """Отображение профиля конкретного пользователя"""
#
#     queryset = services.all_objects(get_user_model().objects,
#                                     prefetch_related=('blog_posts', 'following', 'comments'))
#     serializer_class = serializers.UserDetailSerializer
#     permission_classes = [IsOwnerOrReadOnly]


class PostViewSet(viewsets.ModelViewSet):
    """
    Набор представлений для модели Post
    """

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrAdminUserOrReadOnly)

    def get_queryset(self):
        if self.action == 'list':
            return services.all_objects(Post.published,
                                        select_related=('author', 'cat'),
                                        prefetch_related=('comments',))
        elif self.action == 'retrieve':
            return services.all_objects(Post.published,
                                        select_related=('author', 'cat'),
                                        prefetch_related=('tags', 'comments'))
        return services.all_objects(Post.published,
                                    select_related=('author', 'cat'),
                                    prefetch_related=('tags',))

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.PostListSerializer
        elif self.action == 'retrieve':
            return serializers.PostDetailSerializer
        return serializers.PostCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        slug=slugify(self.request.data['title']))

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        redis_services.incr_views(instance.id)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    """
    Набор представлений для модели Comment
    """

    queryset = services.all_objects(Comment.objects)

    def get_serializer_class(self):
        if self.action in ('list', 'create'):
            return serializers.CommentListSerializer
        return serializers.CommentDetailSerializer

    def get_permissions(self):
        if self.action in ('list', 'create'):
            permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
        else:
            permission_classes = (IsOwnerOrAdminUserOrReadOnly,)
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        post = services.get_instance_by_unique_field(Post, pk=int(self.request.data['post']))
        serializer.save(post=post)


# class CommentListAPIView(generics.ListCreateAPIView):
#     """
#     Отображение списка комментариев
#     """
#
#     # queryset = services.all_objects(Comment.objects,
#     #                                 prefetch_related=('post', 'author'))
#     queryset = services.all_objects(Comment.objects)
#     serializer_class = serializers.CommentListSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#
#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)
#
#
# class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
#     """Отображение выбранного комментария"""
#
#     queryset = services.all_objects(Comment.objects)
#     serializer_class = serializers.CommentDetailSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly,
#                           IsOwnerOrAdminUserOrReadOnly]
#
#     def perform_update(self, serializer):
#         post = services.get_instance_by_unique_field(Post, pk=int(self.request.data['post']))
#         serializer.save(post=post)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Набор представлений для модели Category
    """

    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        if self.action in ('list', 'create'):
            return services.all_objects(Category.objects)
        return services.all_objects(Category.objects,
                                    prefetch_related=('posts',))

    def get_serializer_class(self):
        if self.action in ('list', 'create'):
            return serializers.CategoryListSerializer
        return serializers.CategoryDetailSerializer


# class CategoryListAPIView(generics.ListCreateAPIView):
#     """Отображение списка категорий"""
#
#     queryset = services.all_objects(Category.objects)
#     serializer_class = serializers.CategoryListSerializer
#     permission_classes = [IsAdminOrReadOnly]
#
#
# class CategoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
#     """Детальное отображение выбранной категории"""
#
#     queryset = services.all_objects(Category.objects,
#                                     prefetch_related=('posts',))
#     serializer_class = serializers.CategoryDetailSerializer
#     permission_classes = [IsAdminOrReadOnly]


class TagViewSet(viewsets.ModelViewSet):
    """
    Набор представлений для модели Tag
    """

    def get_queryset(self):
        if self.action in ('list', 'create'):
            return services.all_objects(Tag.objects)
        return services.all_objects(Tag.objects,
                                    prefetch_related=('posts',))

    def get_serializer_class(self):
        if self.action in ('list', 'create'):
            return serializers.TagListSerializer
        return serializers.TagDetailSerializer

    def get_permissions(self):
        if self.action in ('list', 'create'):
            permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
        else:
            permission_classes = (IsAdminOrReadOnly,)
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        services.create_tag_serializer(serializer, self.request.data['name'])


# class TagListAPIView(generics.ListCreateAPIView):
#     """Отображение списка тегов"""
#
#     queryset = services.all_objects(Tag.objects)
#     serializer_class = serializers.TagListSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
#
#     def perform_create(self, serializer):
#         services.create_tag_serializer(serializer, self.request.data['name'])
#
#
# class TagDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
#     """Детальное отображение выбранного тега"""
#
#     queryset = services.all_objects(Tag.objects,
#                                     prefetch_related=('posts',))
#     serializer_class = serializers.TagDetailSerializer
#     permission_classes = [IsAdminOrReadOnly]


class CreateUserFollowingAPIView(APIView):
    """
    Оформление подписки на пользователя
    """

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, pk):
        user = services.get_instance_by_unique_field(get_user_model(), pk=pk)
        follower = request.user
        status = services.subscribe(user, follower)
        return Response({'following': status})

        # user = get_object_or_404(User, pk=pk)
        # profile = request.user
        # if profile in user.followers.all():
        #     user.followers.remove(profile)
        #     return Response({'following': False})
        # user.followers.add(profile)
        # return Response({'following': True})
