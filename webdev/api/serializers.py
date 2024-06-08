from django.contrib.auth import get_user_model
from rest_framework import serializers

from services import services, redis_services
from post.models import Post, Comment, Category, Tag


class UserListSerializer(serializers.ModelSerializer):
    """Сериализатор списка пользователей"""

    class Meta:
        model = get_user_model()
        fields = ('id', 'username')


class UserDetailSerializer(serializers.ModelSerializer):
    """Сериализатор одного пользователя"""

    username = serializers.ReadOnlyField()
    blog_posts = serializers.SlugRelatedField(slug_field='title', many=True, read_only=True)
    comments = serializers.SerializerMethodField()
    # comments = serializers.SlugRelatedField(slug_field='body', many=True, read_only=True, allow_null=True)
    date_joined = serializers.ReadOnlyField()
    following = serializers.SlugRelatedField(slug_field='username', many=True, read_only=True, allow_null=True)

    def get_comments(self, obj):
        """Отображение комментариев пользователя в виде Post.title: Comment.body"""

        comments = services.all_objects(obj.comments)
        if not comments:
            return None
        comments_serialized = CommentListSerializer(comments[:5], many=True).data
        return [f'{comment["post"]}: {comment["body"]}' for comment in comments_serialized]

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'date_joined', 'first_name',
                  'last_name', 'email', 'photo', 'blog_posts',  'comments', 'following')


class PostListSerializer(serializers.ModelSerializer):
    """Сериализатор списка постов"""

    author = serializers.ReadOnlyField(source='author.username')
    cat = serializers.SlugRelatedField(slug_field='cat_title',
                                       queryset=services.all_objects(Category.objects))

    class Meta:
        model = Post
        fields = ('id', 'title', 'author', 'cat',
                  'title_image', 'publish',)

    def to_representation(self, instance):
        """Добавление количества комментариев и просмотров поста"""

        representation = super().to_representation(instance)
        representation['comments'] = instance.comments.count()
        representation['views'] = redis_services.get_views(instance.id)
        return representation


class PostDetailSerializer(serializers.ModelSerializer):
    """Сериализатор одного поста"""

    author = serializers.ReadOnlyField(source='author.username')
    cat = serializers.SlugRelatedField(slug_field='cat_title',
                                       queryset=services.all_objects(Category.objects))
    comments = serializers.SerializerMethodField()
    tags = serializers.SlugRelatedField(slug_field='name',
                                        many=True,
                                        queryset=services.all_objects(Tag.objects))

    def get_comments(self, obj):
        """Отображение комментариев поста в виде User.username: Comment.body"""

        comments = services.all_objects(obj.comments)
        if not comments:
            return None
        comments_serialized = CommentListSerializer(comments, many=True).data
        return [f'{comment["author"]}: {comment["body"]}' for comment in comments_serialized]

    class Meta:
        model = Post
        fields = ('id', 'title', 'author', 'cat',
                  'title_image', 'body', 'tags', 'comments')

    def to_representation(self, instance):
        """Добавление количества просмотров поста"""

        representation = super().to_representation(instance)
        representation['views'] = redis_services.get_views(instance.id)
        return representation


class PostCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания поста"""

    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = ('id', 'title', 'author', 'cat',
                  'title_image', 'body', 'tags')


class CategoryListSerializer(serializers.ModelSerializer):
    """Сериализатор списка категорий"""

    class Meta:
        model = Category
        fields = ['id', 'cat_title']


class CategoryDetailSerializer(serializers.ModelSerializer):
    """Сериализатор одной категории"""

    posts = serializers.SlugRelatedField(slug_field='title', many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'cat_title', 'posts']


class CommentListSerializer(serializers.ModelSerializer):
    """Сериализатор списка комментариев"""

    author = serializers.ReadOnlyField(source='author.username')
    post = serializers.SlugRelatedField(slug_field='title',
                                        queryset=services.all_objects(Post.published))

    class Meta:
        model = Comment
        fields = ['id', 'body', 'author', 'post']


class CommentDetailSerializer(serializers.ModelSerializer):
    """Сериализатор одного комментария"""

    author = serializers.ReadOnlyField(source='author.username')
    post = serializers.SlugRelatedField(slug_field='title', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'body', 'author', 'post']


class TagListSerializer(serializers.ModelSerializer):
    """Сериализатор списка тегов"""

    class Meta:
        model = Tag
        fields = ['id', 'name']


class TagDetailSerializer(serializers.ModelSerializer):
    """Сериализатор одного тега"""

    posts = serializers.SlugRelatedField(slug_field='title', many=True, read_only=True)

    class Meta:
        model = Tag
        fields = ['id', 'name', 'posts']
