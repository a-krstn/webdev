from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.postgres.search import SearchVector
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
# from django.core.cache import cache (cache.get(), cache.set(key, queryset, time))

from services import services, redis_services
from .models import *
from .mixins import *
from .forms import *


def page_not_found(request, exception):
    """
    Обработчик 404 Not Found
    """

    return render(request, 'post/post/404.html', status=404)


def access_is_denied(request, exception):
    """
    Обработчик 403 Forbidden
    """

    return render(request, 'post/post/403.html', status=403)


class PostListView(generic.ListView):
    """
    Вывод списка постов на главной странице
    """

    queryset = services.all_objects(Post.published,
                                    select_related=('cat', 'author'),
                                    prefetch_related=('comments', ),
                                    only=('title', 'slug', 'body', 'title_image',
                                          'publish', 'author__username', 'author__id',
                                          'cat__cat_title', 'cat__slug'))
    template_name = 'post/post/list.html'
    context_object_name = 'posts'
    paginate_by = 3
    extra_context = {'title': 'Главная страница'}


class CategoryListView(generic.ListView):
    """
    Вывод списка постов выбранной категории
    """

    template_name = 'post/post/list.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category = services.get_instance_by_unique_field(Category, slug=self.kwargs.get('slug'))
        context['title'] = f'По категории: {category.cat_title}'
        return context

    def get_queryset(self):
        return services.filter_objects(Post.published,
                                       cat__slug=self.kwargs.get('slug'),
                                       select_related=('cat', 'author'),
                                       prefetch_related=('comments',),
                                       only=('title', 'slug', 'body', 'title_image',
                                             'publish', 'author__username', 'author__id',
                                             'cat__cat_title', 'cat__slug'))


class PostDetailView(generic.DetailView):
    """
    Детальный вывод одного поста
    """

    model = Post
    template_name = 'post/post/detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = services.all_objects(kwargs['object'].comments,
                                                   select_related=('author',))
        context['form'] = CommentForm()
        redis_services.incr_views(context['post'].id)
        context['title'] = self.object.title
        return context

    def get_object(self, queryset=None):
        return services.get_instance_by_unique_field(Post.published,
                                                     slug=self.kwargs.get(self.slug_url_kwarg))


class PostCreateView(PermissionRequiredMixin,
                     generic.CreateView):
    """
    Создание поста
    """

    form_class = PostForm
    template_name = 'post/post/create_post.html'
    extra_context = {'title': 'Создание статьи'}
    permission_required = 'post.add_post'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            services.create_post(form, request.user)
            return redirect('index')
        return render(request, self.template_name, {'form': form})


class PostUpdateView(IsPostOwnerOrAdminMixin,
                     LoginRequiredMixin,
                     generic.UpdateView):
    """
    Редактирование поста
    """

    form_class = PostForm
    template_name = 'post/post/create_post.html'
    extra_context = {'title': 'Редактирование статьи'}
    permission_required = 'post.change_post'

    def get_queryset(self):
        return services.filter_objects(Post.published,
                                       slug=self.kwargs.get('slug'),
                                       select_related=('cat', 'author'),
                                       only=('title', 'slug', 'body', 'title_image',
                                             'publish', 'author__username', 'author__id',
                                             'cat__cat_title', 'cat__slug'))


class PostDeleteView(IsPostOwnerOrAdminMixin,
                     LoginRequiredMixin,
                     generic.DeleteView):
    """
    Удаление поста
    """

    model = Post
    success_url = reverse_lazy('index')
    template_name = 'post/post/post_confirm_delete.html'
    permission_required = 'post.delete_post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удаление поста: {self.object.title}'
        return context

    def get_queryset(self):
        return services.filter_objects(Post.published,
                                       slug=self.kwargs.get('slug'),
                                       select_related=('cat', 'author'),
                                       only=('title', 'slug', 'body', 'title_image',
                                             'publish', 'author__username', 'author__id',
                                             'cat__cat_title', 'cat__slug'))


class PostCommentView(PermissionRequiredMixin,
                      LoginRequiredMixin,
                      generic.CreateView):
    """
    Добавление комментария
    """

    form_class = CommentForm
    template_name = 'post/post/detail.html'
    permission_required = 'post.add_comment'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        post = services.get_instance_by_unique_field(Post, pk=kwargs['post_id'])
        if form.is_valid():
            services.create_comment(form, request.user, post)
            return redirect(post.get_absolute_url())
        return render(request, self.template_name, {'form': form})


class CommentUpdateView(IsCommentOwnerOrAdminMixin,
                        LoginRequiredMixin,
                        generic.UpdateView):
    """
    Редактирование комментария
    """

    form_class = CommentForm
    template_name = 'post/post/edit_comment.html'
    extra_context = {'title': 'Редактирование комментария'}
    permission_required = 'post.change_comment'

    def get_queryset(self):
        return services.filter_objects(Comment.objects,
                                       pk=self.kwargs.get('pk'),
                                       prefetch_related=('author',),
                                       only=('body',))

    def get_success_url(self):
        comment = services.get_instance_by_unique_field(Comment, pk=self.kwargs['pk'])
        post = comment.post
        return post.get_absolute_url()


class CommentDeleteView(IsCommentOwnerOrAdminMixin,
                        LoginRequiredMixin,
                        generic.DeleteView):
    """
    Удаление комментария
    """

    model = Comment
    template_name = 'post/post/comment_confirm_delete.html'
    extra_context = {'title': 'Удаление комментария'}
    pk_url_kwarg = 'pk'
    permission_required = 'post.delete_comment'

    def get_success_url(self):
        comment = self.object
        post = comment.post
        return post.get_absolute_url()

    def get_queryset(self):
        return services.filter_objects(Comment.objects,
                                       pk=self.kwargs.get('pk'),
                                       prefetch_related=('author',),
                                       only=('body',))


class AboutView(generic.TemplateView):
    """
    Отображение страницы "О сайте"
    """

    text = """Веб-приложение создано с использованием Django + DRF"""
    template_name = 'post/post/about.html'
    extra_context = {'title': 'О сайте',
                     'text': text}


class ContactsView(generic.TemplateView):
    """
    Отображение страницы "Контакты"
    """

    text = """Проект на GitHub"""
    template_name = 'post/post/contacts.html'
    extra_context = {'title': 'Контакты',
                     'text': text}


class PostListByTagView(generic.ListView):
    """
    Вывод списка постов по выбранному тегу
    """

    model = Post
    template_name = 'post/post/list.html'
    context_object_name = 'posts'
    paginate_by = 3
    tag = None

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = services.get_instance_by_unique_field(Tag, slug=self.kwargs.get('tag_slug'))
        context['title'] = f'По тегу: {tag.name}'
        return context

    def get_queryset(self):
        return services.filter_objects(Post.published,
                                       tags__slug=self.kwargs.get('tag_slug'),
                                       select_related=('cat', 'author'),
                                       prefetch_related=('comments',),
                                       only=('title', 'slug', 'body', 'title_image',
                                             'publish', 'author__username', 'author__id',
                                             'cat__cat_title', 'cat__slug'))


class PostListByFollowingView(LoginRequiredMixin,
                              generic.ListView):
    """
    Вывод списка постов пользователей, на которых оформлена подписка
    """

    model = Post
    template_name = 'post/post/list.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        user_subscriptions = services.all_objects(self.request.user.following)
        queryset = services.filter_objects(Post.published,
                                           author__in=user_subscriptions,
                                           select_related=('author', 'cat'),
                                           prefetch_related=('comments',),
                                           only=('title', 'slug', 'body', 'title_image',
                                                 'publish', 'author__username', 'author__id',
                                                 'cat__cat_title', 'cat__slug'))
        return queryset

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Посты по подписке'
        return context


def post_search(request):
    """
    Поиск по сайту
    """

    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.published.annotate(search=SearchVector('title', 'body'), ).filter(search=query)

    return render(request, 'post/post/search.html', {'form': form,
                                                     'query': query,
                                                     'results': results,
                                                     'title': 'Поиск'})
