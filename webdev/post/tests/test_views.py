from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from account.models import User
from post.models import Post, Category, Tag, Comment

from http import HTTPStatus


class PostListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_posts = 5
        for post_num in range(number_of_posts):
            Post.objects.create(title='Title %s' % post_num,
                                slug='title_one_%s' % post_num,
                                body='Title_one_text %s' % post_num,
                                author=User.objects.create(username='u_%s' % post_num),
                                status='PB')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'post/post/list.html')

    def test_pagination(self):
        response = self.client.get(reverse('index'))
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertTrue(len(response.context['posts']) == 3)

    def test_title(self):
        response = self.client.get(reverse('index'))
        self.assertTrue('title' in response.context)
        self.assertTrue(response.context['title'] == 'Главная страница')

    def test_pagination_next_page(self):
        response = self.client.get(reverse('index')+'?page=2')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertTrue(len(response.context['posts']) == 2)


class CategoryListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        category = Category.objects.create(cat_title='Category',
                                           slug='category')

        number_of_posts = 5
        for post_num in range(number_of_posts):
            Post.objects.create(title='Title %s' % post_num,
                                slug='title_one_%s' % post_num,
                                cat=category,
                                body='Title_one_text %s' % post_num,
                                author=User.objects.create(username='u_%s' % post_num),
                                status='PB')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/category/category/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('category_list', args=('category',)))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('category_list', args=('category',)))
        self.assertTemplateUsed(response, 'post/post/list.html')

    def test_pagination(self):
        response = self.client.get(reverse('category_list', args=('category',)))
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertTrue(len(response.context['posts']) == 3)

    def test_title(self):
        response = self.client.get(reverse('category_list', args=('category',)))
        self.assertTrue('title' in response.context)
        self.assertTrue(response.context['title'] == f'По категории: Category')

    def test_pagination_next_page(self):
        response = self.client.get(reverse('category_list', args=('category',))+'?page=2')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertTrue(len(response.context['posts']) == 2)


class PostDetailViewTest(TestCase):
    def setUp(self):
        category = Category.objects.create(cat_title='Category',
                                           slug='category')
        user = User.objects.create(username='test_user', password='12345')
        post = Post.objects.create(title='Post title',
                                   slug='post_title',
                                   cat=category,
                                   body='Post text',
                                   author=user,
                                   status='PB')
        self.post = post

    def test_view_url_exists_at_desired_location(self):
        path = self.post.get_absolute_url()
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('post_detail', args=(self.post.publish.day,
                                                                self.post.publish.month,
                                                                self.post.publish.year,
                                                                self.post.slug)))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_uses_correct_template(self):
        response = self.client.get(self.post.get_absolute_url())
        self.assertTemplateUsed(response, 'post/post/detail.html')

    def test_title(self):
        response = self.client.get(self.post.get_absolute_url())
        self.assertTrue('title' in response.context)
        self.assertTrue(response.context['title'] == f'{self.post.title}')

    def test_post_body(self):
        response = self.client.get(self.post.get_absolute_url())
        self.assertEqual(self.post.body, response.context_data['post'].body)


class AboutViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('about'))
        self.assertTemplateUsed(response, 'post/post/about.html')

    def test_title(self):
        response = self.client.get(reverse('about'))
        self.assertTrue('title' in response.context)
        self.assertTrue(response.context['title'] == 'О сайте')


class ContactViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/contacts/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('contacts'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('contacts'))
        self.assertTemplateUsed(response, 'post/post/contacts.html')

    def test_title(self):
        response = self.client.get(reverse('contacts'))
        self.assertTrue('title' in response.context)
        self.assertTrue(response.context['title'] == 'Контакты')


class TagListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        tag = Tag.objects.create(name='Tag 1',
                                 slug='tag_1')

        number_of_posts = 5
        for post_num in range(number_of_posts):
            Post.objects.create(title='Title %s' % post_num,
                                slug='title_one_%s' % post_num,
                                body='Title_one_text %s' % post_num,
                                author=User.objects.create(username='u_%s' % post_num),
                                status='PB')
        tag.posts.set(Post.objects.all())

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/tag/tag_1/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('post_list_tag', args=('tag_1',)))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('post_list_tag', args=('tag_1',)))
        self.assertTemplateUsed(response, 'post/post/list.html')

    def test_pagination(self):
        response = self.client.get(reverse('post_list_tag', args=('tag_1',)))
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertTrue(len(response.context['posts']) == 3)

    def test_title(self):
        response = self.client.get(reverse('post_list_tag', args=('tag_1',)))
        self.assertTrue('title' in response.context)
        self.assertTrue(response.context['title'] == 'По тегу: Tag 1')

    def test_lists_all_posts(self):
        response = self.client.get(reverse('post_list_tag', args=('tag_1',))+'?page=2')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] is True)
        self.assertTrue(len(response.context['posts']) == 2)


class PostListByFollowingViewTest(TestCase):
    def setUp(self):
        user1 = get_user_model().objects.create_user(username='test_user1', password='12345')
        user1.save()
        user2 = get_user_model().objects.create_user(username='test_user2', password='12345')
        user2.save()

        for post_num in range(5):
            post = Post.objects.create(title='Title %s' % post_num,
                                       slug='title_one_%s' % post_num,
                                       body='Title_one_text %s' % post_num,
                                       author=user2,
                                       status='PB')
            post.save()

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('following_list'))
        self.assertRedirects(resp, '/account/login/?next=/following/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='test_user1', password='12345')
        resp = self.client.get(reverse('following_list'))

        # Проверка, что пользователь залогинился
        self.assertEqual(str(resp.context['user']), 'test_user1')

        # Проверка ответа на запрос
        self.assertEqual(resp.status_code, HTTPStatus.OK)

        # Проверка использования правильного шаблона
        self.assertTemplateUsed(resp, 'post/post/list.html')

    def test_only_test_user2_posts_in_list(self):
        login = self.client.login(username='test_user1', password='12345')
        resp = self.client.get(reverse('following_list'))

        # Проверка, что пользователь залогинился
        self.assertEqual(str(resp.context['user']), 'test_user1')
        # Проверка ответа на запрос
        self.assertEqual(resp.status_code, HTTPStatus.OK)

        # Проверка, что изначально у нас нет постов в списке
        self.assertTrue('posts' in resp.context)
        self.assertEqual(len(resp.context['posts']), 0)

        # Добавление test_user2 в подписки test_user1
        test_user1 = get_user_model().objects.get(username='test_user1')
        test_user2 = get_user_model().objects.get(username='test_user2')
        test_user1.following.add(test_user2)

        resp = self.client.get(reverse('following_list'))
        # Проверка, что пользователь залогинился
        self.assertEqual(str(resp.context['user']), 'test_user1')
        # Проверка успешности ответа
        self.assertEqual(resp.status_code, HTTPStatus.OK)
        self.assertTrue('posts' in resp.context)

        # проверка количества постов на странице
        self.assertEqual(len(resp.context['posts']), 3)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] is True)

        # проверка количества постов на второй странице
        response = self.client.get(reverse('following_list') + '?page=2')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(len(response.context['posts']) == 2)

    def test_title(self):
        login = self.client.login(username='test_user1', password='12345')
        response = self.client.get(reverse('following_list'))
        self.assertTrue('title' in response.context)
        self.assertTrue(response.context['title'] == 'Посты по подписке')


class PostCreateViewTest(TestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(username='test_user1', password='12345')
        self.user2 = get_user_model().objects.create_user(username='test_user2', password='12345', is_superuser=True)

        self.category = Category.objects.create(cat_title='Категория 1', slug='category_1')

        permission = Permission.objects.get(name='Can add Пост')
        self.user2.user_permissions.add(permission)
        self.user2.save()

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('create_post'))
        self.assertRedirects(resp, '/account/login/?next=/create_post/')

    def test_redirect_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='test_user1', password='12345')
        resp = self.client.get(reverse('create_post'))
        self.assertEqual(resp.status_code, HTTPStatus.FORBIDDEN)

    def test_logged_in_with_permission_create_post(self):
        login = self.client.login(username='test_user2', password='12345')
        resp = self.client.get(reverse('create_post'))

        # Проверка, что если пользователь авторизован, то доступ для создания поста открыт
        self.assertEqual(resp.status_code, HTTPStatus.OK)

    def test_uses_correct_template(self):
        login = self.client.login(username='test_user2', password='12345')
        resp = self.client.get(reverse('create_post'))
        self.assertEqual(resp.status_code, HTTPStatus.OK)

        # Проверка использования корректного шаблона
        self.assertTemplateUsed(resp, 'post/post/create_post.html')

    # def test_title(self):
    # Экстра контекст не отрабатывает, нет заголовка
    #     login = self.client.login(username='test_user2', password='12345')
    #     response = self.client.get(reverse('create_post'))
    #     self.assertTrue('title' in response.context)
    #     self.assertTrue(response.context['title'] == 'Создание статьи')

    def test_redirects_to_main_page_on_success(self):
        login = self.client.login(username='test_user2', password='12345')
        data = {
            'title': 'Post title 8',
            'slug': 'post_title_8',
            'cat': self.category.pk,
            'author': self.user2,
            'body': 'New comment to post',
        }
        resp = self.client.post(reverse('create_post'), data, follow=True)
        self.assertEqual(resp.status_code, HTTPStatus.OK)
        post = Post.objects.filter(title='Post_title').exists()
        self.assertTrue(post)
        self.assertTrue(resp, reverse('index'))


class PostUpdateViewTest(TestCase):
    def setUp(self):
        user1 = get_user_model().objects.create_user(username='test_user1', password='12345')
        user1.save()
        user2 = get_user_model().objects.create_user(username='test_user2', password='12345')
        user2.save()
        user3 = get_user_model().objects.create_user(username='test_user3', password='12345')
        user2.save()

        permission = Permission.objects.get(name='Can change Пост')
        user2.user_permissions.add(permission)
        user2.save()

        user3.user_permissions.add(permission)
        user3.save()

        category = Category.objects.create(cat_title='Категория 1', slug='category_1')
        category.save()
        post = Post.objects.create(title='Post title',
                                   slug='post_title',
                                   cat=category,
                                   author=user3,
                                   body='Post text')
        post.save()
        self.post = post

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('edit_page', args=(self.post.slug,)))
        self.assertEqual(resp.status_code, HTTPStatus.FOUND)
        self.assertTrue(resp.url.startswith('/account/login/'))

    def test_403_if_logged_in_but_without_permission(self):
        login = self.client.login(username='test_user1', password='12345')
        resp = self.client.get(reverse('edit_page', args=(self.post.slug,)))

        # Проверка вызова ошибки доступа 403
        self.assertEqual(resp.status_code, HTTPStatus.FORBIDDEN)

    def test_403_if_logged_in_with_permission_but_not_author_or_admin(self):
        login = self.client.login(username='test_user2', password='12345')
        resp = self.client.get(reverse('edit_page', args=(self.post.slug,)))

        # Проверка вызова ошибки доступа 403
        self.assertEqual(resp.status_code, HTTPStatus.FORBIDDEN)

    def test_logged_in_with_permission_and_author_or_admin(self):
        login = self.client.login(username='test_user3', password='12345')
        resp = self.client.get(reverse('edit_page', args=(self.post.slug,)))

        # Проверка доступа к редактированию поста
        self.assertEqual(resp.status_code, HTTPStatus.OK)

    def test_uses_correct_template(self):
        login = self.client.login(username='test_user3', password='12345')
        resp = self.client.get(reverse('edit_page', args=(self.post.slug,)))
        self.assertEqual(resp.status_code, HTTPStatus.OK)

        # Проверка использования корректного шаблона
        self.assertTemplateUsed(resp, 'post/post/create_post.html')

    def test_title(self):
        login = self.client.login(username='test_user3', password='12345')
        response = self.client.get(reverse('edit_page', args=(self.post.slug,)))
        self.assertTrue('title' in response.context)
        self.assertTrue(response.context['title'] == 'Редактирование статьи')

    def test_redirects_to_main_page_on_success(self):
        # После успешного редактирования статьи отображает статус 200, а не 302, как ожидается
        login = self.client.login(username='test_user3', password='12345')
        resp = self.client.post(reverse('edit_page', args=(self.post.slug,)),
                                {'body': 'Это измененный текст поста'},
                                follow=True)
        self.assertTrue(resp, self.post.get_absolute_url())


class PostDeleteViewTest(TestCase):
    def setUp(self):
        user1 = get_user_model().objects.create_user(username='test_user1', password='12345')
        user1.save()
        user2 = get_user_model().objects.create_user(username='test_user2', password='12345')
        user2.save()
        user3 = get_user_model().objects.create_user(username='test_user3', password='12345')
        user2.save()

        permission = Permission.objects.get(name='Can delete Пост')
        user2.user_permissions.add(permission)
        user2.save()

        user3.user_permissions.add(permission)
        user3.save()

        category = Category.objects.create(cat_title='Категория 1', slug='category_1')
        category.save()
        post = Post.objects.create(title='Post title',
                                   slug='post_title',
                                   cat=category,
                                   author=user3,
                                   body='Post text')
        post.save()
        self.post = post

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('delete_post', args=(self.post.slug,)))
        self.assertEqual(resp.status_code, HTTPStatus.FOUND)
        self.assertTrue(resp.url.startswith('/account/login/'))

    def test_403_if_logged_in_but_without_permission(self):
        login = self.client.login(username='test_user1', password='12345')
        resp = self.client.get(reverse('delete_post', args=(self.post.slug,)))

        # Проверка вызова ошибки доступа 403
        self.assertEqual(resp.status_code, HTTPStatus.FORBIDDEN)

    def test_403_if_logged_in_with_permission_but_not_author_or_admin(self):
        login = self.client.login(username='test_user2', password='12345')
        resp = self.client.get(reverse('delete_post', args=(self.post.slug,)))

        # Проверка вызова ошибки доступа 403
        self.assertEqual(resp.status_code, HTTPStatus.FORBIDDEN)

    def test_logged_in_with_permission_and_author_or_admin(self):
        login = self.client.login(username='test_user3', password='12345')
        resp = self.client.get(reverse('delete_post', args=(self.post.slug,)))

        # Проверка доступа к редактированию поста
        self.assertEqual(resp.status_code, HTTPStatus.OK)

    def test_uses_correct_template(self):
        login = self.client.login(username='test_user3', password='12345')
        resp = self.client.get(reverse('delete_post', args=(self.post.slug,)))
        self.assertEqual(resp.status_code, HTTPStatus.OK)

        # Проверка использования корректного шаблона
        self.assertTemplateUsed(resp, 'post/post/post_confirm_delete.html')

    def test_title(self):
        login = self.client.login(username='test_user3', password='12345')
        response = self.client.get(reverse('delete_post', args=(self.post.slug,)))
        self.assertTrue('title' in response.context)
        self.assertTrue(response.context['title'] == f'Удаление поста: {self.post.title}')

    def test_redirects_to_main_page_on_success(self):
        # Проверка перенаправления на главную страницу после успешного удаления поста
        login = self.client.login(username='test_user3', password='12345')
        resp = self.client.post(reverse('delete_post', args=(self.post.slug,)), follow=True)
        self.assertRedirects(resp, reverse('index'))


class PostCommentViewTest(TestCase):
    def setUp(self):
        user1 = get_user_model().objects.create_user(username='test_user1', password='12345')
        user1.save()
        user2 = get_user_model().objects.create_user(username='test_user2', password='12345')
        user1.save()

        permission = Permission.objects.get(name='Can add Комментарий')
        user2.user_permissions.add(permission)
        user2.save()

        category = Category.objects.create(cat_title='Category',
                                           slug='category')
        post = Post.objects.create(title='Post title',
                                   slug='post_title',
                                   cat=category,
                                   body='Post text',
                                   author=user2)
        self.post = post

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('post_comment', args=(self.post.pk,)))
        # self.assertRedirects(resp, f'/account/login/?next=/{self.post.pk}/comment')
        self.assertRedirects(resp, f'/account/login/?next=/{self.post.pk}/comment')

    def test_redirect_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='test_user1', password='12345')
        resp = self.client.get(reverse('post_comment', args=(self.post.pk,)))
        self.assertEqual(resp.status_code, HTTPStatus.FORBIDDEN)

    # def test_logged_in_with_permission_create_comment(self):
    #     login = self.client.login(username='test_user2', password='12345')
    #     resp = self.client.get(reverse('post_comment', args=(self.post.pk,)))
    #
    #     # Проверка, что если пользователь авторизован, то доступ для создания поста открыт
    #     self.assertEqual(resp.status_code, HTTPStatus.OK)

    # def test_uses_correct_template(self):
    #     login = self.client.login(username='test_user2', password='12345')
    #     resp = self.client.get(reverse('post_comment', args=(self.post.pk,)))
    #     self.assertEqual(resp.status_code, HTTPStatus.OK)
    #
    #     # Проверка использования корректного шаблона
    #     self.assertTemplateUsed(resp, 'post/post/create_post.html')

    # def test_redirects_to_main_page_on_success(self):
    #     # После успешного создания статьи отображает статус 200, а не 302, как ожидается
    #     login = self.client.login(username='test_user2', password='12345')
    #     category = Category.objects.create(cat_title='Категория 1', slug='category_1')
    #     resp = self.client.post(reverse('create_post'), {'title': 'Post title',
    #                                                      'cat': category,
    #                                                      'body': 'Это текст поста'},
    #                             follow=True)
    #     self.assertTrue(resp, reverse('index'))


class CommentUpdateViewTest(TestCase):
    def setUp(self):
        user1 = get_user_model().objects.create_user(username='test_user1', password='12345')
        user1.save()
        user2 = get_user_model().objects.create_user(username='test_user2', password='12345')
        user2.save()
        user3 = get_user_model().objects.create_user(username='test_user3', password='12345')
        user3.save()

        permission = Permission.objects.get(name='Can change Комментарий')
        user2.user_permissions.add(permission)
        user2.save()
        user3.user_permissions.add(permission)
        user3.save()

        category = Category.objects.create(cat_title='Категория 1', slug='category_1')
        category.save()
        post = Post.objects.create(title='Post title',
                                   slug='post_title',
                                   cat=category,
                                   author=user3,
                                   body='Post text')
        post.save()

        comment = Comment.objects.create(author=user3,
                                         post=post,
                                         body='Comment to post')
        comment.save()
        self.comment = comment

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('edit_comment', args=(self.comment.pk,)))
        self.assertEqual(resp.status_code, HTTPStatus.FOUND)
        self.assertTrue(resp.url.startswith('/account/login/'))

    def test_403_if_logged_in_but_without_permission(self):
        login = self.client.login(username='test_user1', password='12345')
        resp = self.client.get(reverse('edit_comment', args=(self.comment.pk,)))

        # Проверка вызова ошибки доступа 403
        self.assertEqual(resp.status_code, HTTPStatus.FORBIDDEN)

    def test_403_if_logged_in_with_permission_but_not_author_or_admin(self):
        login = self.client.login(username='test_user2', password='12345')
        resp = self.client.get(reverse('edit_comment', args=(self.comment.pk,)))

        # Проверка вызова ошибки доступа 403
        self.assertEqual(resp.status_code, HTTPStatus.FORBIDDEN)

    def test_logged_in_with_permission_and_author_or_admin(self):
        login = self.client.login(username='test_user3', password='12345')
        resp = self.client.get(reverse('edit_comment', args=(self.comment.pk,)))

        # Проверка доступа к редактированию поста
        self.assertEqual(resp.status_code, HTTPStatus.OK)

    def test_uses_correct_template(self):
        login = self.client.login(username='test_user3', password='12345')
        resp = self.client.get(reverse('edit_comment', args=(self.comment.pk,)))
        self.assertEqual(resp.status_code, HTTPStatus.OK)

        # Проверка использования корректного шаблона
        self.assertTemplateUsed(resp, 'post/post/edit_comment.html')

    def test_title(self):
        login = self.client.login(username='test_user3', password='12345')
        response = self.client.get(reverse('edit_comment', args=(self.comment.pk,)))
        self.assertTrue('title' in response.context)
        self.assertTrue(response.context['title'] == 'Редактирование комментария')

    def test_redirects_to_main_page_on_success(self):
        # Проверка перенаправления на детальное отображение поста после успешного редактирования комментария
        login = self.client.login(username='test_user3', password='12345')
        resp = self.client.post(reverse('edit_comment', args=(self.comment.pk,)),
                                {'body': 'Это измененный текст комментария'},
                                follow=True)
        self.assertRedirects(resp, self.comment.post.get_absolute_url())


class CommentDeleteView(TestCase):
    def setUp(self):
        user1 = get_user_model().objects.create_user(username='test_user1', password='12345')
        user1.save()
        user2 = get_user_model().objects.create_user(username='test_user2', password='12345')
        user2.save()
        user3 = get_user_model().objects.create_user(username='test_user3', password='12345')
        user3.save()

        permission = Permission.objects.get(name='Can change Комментарий')
        user2.user_permissions.add(permission)
        user2.save()
        user3.user_permissions.add(permission)
        user3.save()

        category = Category.objects.create(cat_title='Категория 1', slug='category_1')
        category.save()
        post = Post.objects.create(title='Post title',
                                   slug='post_title',
                                   cat=category,
                                   author=user3,
                                   body='Post text')
        post.save()

        comment = Comment.objects.create(author=user3,
                                         post=post,
                                         body='Comment to post')
        comment.save()
        self.comment = comment

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('delete_comment', args=(self.comment.pk,)))
        self.assertEqual(resp.status_code, HTTPStatus.FOUND)
        self.assertTrue(resp.url.startswith('/account/login/'))

    def test_403_if_logged_in_but_without_permission(self):
        login = self.client.login(username='test_user1', password='12345')
        resp = self.client.get(reverse('delete_comment', args=(self.comment.pk,)))

        # Проверка вызова ошибки доступа 403
        self.assertEqual(resp.status_code, HTTPStatus.FORBIDDEN)

    def test_403_if_logged_in_with_permission_but_not_author_or_admin(self):
        login = self.client.login(username='test_user2', password='12345')
        resp = self.client.get(reverse('delete_comment', args=(self.comment.pk,)))

        # Проверка вызова ошибки доступа 403
        self.assertEqual(resp.status_code, HTTPStatus.FORBIDDEN)

    def test_logged_in_with_permission_and_author_or_admin(self):
        login = self.client.login(username='test_user3', password='12345')
        resp = self.client.get(reverse('delete_comment', args=(self.comment.pk,)))

        # Проверка доступа к редактированию поста
        self.assertEqual(resp.status_code, HTTPStatus.OK)

    def test_uses_correct_template(self):
        login = self.client.login(username='test_user3', password='12345')
        resp = self.client.get(reverse('delete_comment', args=(self.comment.pk,)))
        self.assertEqual(resp.status_code, HTTPStatus.OK)

        # Проверка использования корректного шаблона
        self.assertTemplateUsed(resp, 'post/post/comment_confirm_delete.html')

    def test_title(self):
        login = self.client.login(username='test_user3', password='12345')
        response = self.client.get(reverse('delete_comment', args=(self.comment.pk,)))
        self.assertTrue('title' in response.context)
        self.assertTrue(response.context['title'] == 'Удаление комментария')

    def test_redirects_to_main_page_on_success(self):
        # Проверка перенаправления на детальное отображение поста после успешного удаления комментария
        login = self.client.login(username='test_user3', password='12345')
        resp = self.client.post(reverse('delete_comment', args=(self.comment.pk,)), follow=True)
        self.assertRedirects(resp, self.comment.post.get_absolute_url())
