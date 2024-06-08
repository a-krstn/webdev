from django.contrib import admin, messages
from django_summernote.admin import SummernoteModelAdmin

from .models import Post, Comment, Category, Tag


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    # fields = ['title', 'slug']    # отображаемые полей при создании нового поста через админку
    # readonly_fields = ['author']  # поля только для чтения при изменении поста через админку
    list_display = ['title', 'slug', 'publish', 'status', 'brief_info']
    list_display_links = ['title']
    list_filter = ['publish', 'cat', 'tags']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['status']
    actions = ['set_status', 'del_status']
    summernote_fields = ('body',)

    @admin.display(description='Краткое описание', ordering='text')
    def brief_info(self, post: Post):
        return f'Описание {len(post.body)} символов.'

    @admin.action(description='Опубликовать выбранные Посты')
    def set_status(self, request, queryset):
        count = queryset.update(status=Post.Status.PUBLISHED)
        self.message_user(request, f'Изменено {count} Постов')

    @admin.action(description='Снять с публикации выбранные Посты')
    def del_status(self, request, queryset):
        count = queryset.update(status=Post.Status.DRAFT)
        self.message_user(request, f'{count} Постов снято с публикации', messages.WARNING)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'body']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['cat_title']
    prepopulated_fields = {'slug': ('cat_title',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
