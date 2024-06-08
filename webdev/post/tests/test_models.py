from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from post.models import Post, Category, Comment, Tag


class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Post.objects.create(title='Заголовок поста 1',
                            slug='zagolovok_posta_1',
                            body='Интересный текст поста.',
                            author=get_user_model().objects.create_user(username='admin1', password='12345'),
                            cat=Category.objects.create(cat_title='Категория 1', slug='category_1'))

    def test_title_label(self):
        post = Post.objects.last()
        field_label = post._meta.get_field('title').verbose_name
        self.assertEqual(field_label, 'Заголовок')

    def test_title_max_length(self):
        post = Post.objects.last()
        max_length = post._meta.get_field('title').max_length
        self.assertEqual(max_length, 250)

    def test_slug_label(self):
        post = Post.objects.last()
        field_label = post._meta.get_field('slug').verbose_name
        self.assertEqual(field_label, 'Слаг')

    def test_slug_max_length(self):
        post = Post.objects.last()
        max_length = post._meta.get_field('slug').max_length
        self.assertEqual(max_length, 250)

    def test_body_label(self):
        post = Post.objects.last()
        field_label = post._meta.get_field('body').verbose_name
        self.assertEqual(field_label, 'Текст')

    def test_author_label(self):
        post = Post.objects.last()
        field_label = post._meta.get_field('author').verbose_name
        self.assertEqual(field_label, 'Автор')

    def test_cat_label(self):
        post = Post.objects.last()
        field_label = post._meta.get_field('cat').verbose_name
        self.assertEqual(field_label, 'Категория')

    def test_status_label(self):
        post = Post.objects.last()
        field_label = post._meta.get_field('status').verbose_name
        self.assertEqual(field_label, 'Статус')

    def test_created_label(self):
        post = Post.objects.last()
        field_label = post._meta.get_field('created').verbose_name
        self.assertEqual(field_label, 'Создан')

    def test_updated_label(self):
        post = Post.objects.last()
        field_label = post._meta.get_field('updated').verbose_name
        self.assertEqual(field_label, 'Обновлен')

    def test_object_name_is_title(self):
        post = Post.objects.last()
        expected_object_name = post.title
        self.assertEqual(expected_object_name, str(post))

    def test_get_absolute_url(self):
        post = Post.objects.last()
        today = datetime.now()
        self.assertEqual(post.get_absolute_url(), f'/{today.day}/{today.month}/{today.year}/zagolovok_posta_1')


class CommentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        post = Post.objects.create(title='Заголовок поста 2',
                                   slug='zagolovok_posta_2',
                                   body='Интересный текст поста.',
                                   author=get_user_model().objects.create_user(username='admin2', password='12345'),
                                   cat=Category.objects.create(cat_title='Категория 2', slug='category_2'))

        Comment.objects.create(author=get_user_model().objects.create(username='user1'),
                               post=post,
                               body='Комментарий к посту от пользователя')

    def test_author_label(self):
        comment = Comment.objects.last()
        field_label = comment._meta.get_field('author').verbose_name
        self.assertEqual(field_label, 'Пользователь')

    def test_post_label(self):
        comment = Comment.objects.last()
        field_label = comment._meta.get_field('post').verbose_name
        self.assertEqual(field_label, 'Пост')

    def test_object_name_is_title(self):
        comment = Comment.objects.last()
        expected_object_name = f'Комментарий от {comment.author}'
        self.assertEqual(expected_object_name, str(comment))


class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(cat_title='Категория 3',
                                slug='category_3')

    def test_cat_title_label(self):
        category = Category.objects.last()
        field_label = category._meta.get_field('cat_title').verbose_name
        self.assertEqual(field_label, 'Категория')

    def test_cat_title_max_length(self):
        category = Category.objects.last()
        max_length = category._meta.get_field('cat_title').max_length
        self.assertEqual(max_length, 25)

    def test_slug_label(self):
        category = Category.objects.last()
        field_label = category._meta.get_field('slug').verbose_name
        self.assertEqual(field_label, 'Слаг')

    def test_slug_max_length(self):
        category = Category.objects.last()
        max_length = category._meta.get_field('slug').max_length
        self.assertEqual(max_length, 30)

    def test_object_name_is_title(self):
        category = Category.objects.last()
        expected_object_name = category.cat_title
        self.assertEqual(expected_object_name, str(category))


class TagModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Tag.objects.create(name='Тег 1',
                           slug='tag_1')

    def test_name_label(self):
        tag = Tag.objects.last()
        field_label = tag._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'Название')

    def test_name_max_length(self):
        tag = Tag.objects.last()
        max_length = tag._meta.get_field('name').max_length
        self.assertEqual(max_length, 25)

    def test_slug_label(self):
        tag = Tag.objects.last()
        field_label = tag._meta.get_field('slug').verbose_name
        self.assertEqual(field_label, 'Слаг')

    def test_slug_max_length(self):
        tag = Tag.objects.last()
        max_length = tag._meta.get_field('slug').max_length
        self.assertEqual(max_length, 30)

    def test_object_name_is_title(self):
        tag = Tag.objects.last()
        expected_object_name = tag.name
        self.assertEqual(expected_object_name, str(tag))
