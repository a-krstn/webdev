from account.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone

from easy_thumbnails.fields import ThumbnailerImageField


class PublishedModel(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='PB')


class BaseContent(models.Model):
    body = models.TextField(verbose_name='Текст', blank=False)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')

    class Meta:
        abstract = True


class Post(BaseContent):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250, verbose_name='Заголовок')
    slug = models.SlugField(max_length=250,
                            db_index=True,
                            unique_for_date='publish',
                            verbose_name='Слаг')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='Автор',
                               related_name='blog_posts')
    cat = models.ForeignKey('Category',
                            on_delete=models.PROTECT,
                            null=True,
                            related_name='posts',
                            verbose_name='Категория')
    title_image = ThumbnailerImageField(upload_to='post/%Y/%m/%d/',
                                        blank=True,
                                        null=True,
                                        verbose_name='Превью',
                                        resize_source=dict(quality=95,
                                                           size=(1600, 856),
                                                           sharpen=True))
    publish = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default='PB',
                              verbose_name='Статус')
    tags = models.ManyToManyField('Tag', related_name='posts', blank=True)
    objects = models.Manager()
    published = PublishedModel()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish'])  # параметр индекс-ния
        ]
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.publish.day,
                                            self.publish.month,
                                            self.publish.year,
                                            self.slug])


class Comment(BaseContent):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='Пользователь',
                               related_name='comments')
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             verbose_name='Пост',
                             related_name='comments')

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['created'])  # параметр индекс-ния
        ]
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Комментарий от {self.author}'


class Category(models.Model):
    cat_title = models.CharField(max_length=25, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=30, unique=True, db_index=True, verbose_name='Слаг')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.cat_title


class Tag(models.Model):
    name = models.CharField(max_length=25, db_index=True, verbose_name='Название')
    slug = models.SlugField(max_length=30, unique=True, db_index=True, verbose_name='Слаг')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name
