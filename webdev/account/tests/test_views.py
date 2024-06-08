from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase
from django.urls import reverse

from post.models import Post


class RegisterUserViewTest(TestCase):
    def setUp(self):
        group = Group.objects.create(name='Пользователи')

        self.data = {
            'username': 'test_user',
            'email': 'test_user@mail.ru',
            'password1': '12345678Aa',
            'password2': '12345678Aa',
        }

    def test_registration_form(self):
        response = self.client.get(reverse('account:register'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'account/register.html')
        self.assertTrue('title' in response.context)
        self.assertTrue(response.context['title'] == 'Регистрация')

    def test_user_registration_success(self):
        response = self.client.post(reverse('account:register'), self.data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('account:login'))
        self.assertTrue(get_user_model().objects.filter(username=self.data['username']).exists())

    def test_user_registration_password_error(self):
        self.data['password2'] = '12345678A'
        response = self.client.post(reverse('account:register'), self.data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Введенные пароли не совпадают.')

    def test_user_registration_exists_error(self):
        get_user_model().objects.create_user(username=self.data['username'])
        response = self.client.post(reverse('account:register'), self.data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким именем уже существует.')

    def test_redirect_mainpage_if_registered_and_logged(self):
        self.client.post(reverse('account:register'), self.data)
        self.client.login(username=self.data['username'], password=self.data['password1'])
        response = self.client.get(reverse('account:register'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('index'))


class LoginUserViewTest(TestCase):
    def setUp(self):
        group = Group.objects.create(name='Пользователи')

        self.data = {
            'username': 'test_user',
            'email': 'test_user@mail.ru',
            'password1': '12345678Aa',
            'password2': '12345678Aa',
        }

    def test_login_form(self):
        response = self.client.get(reverse('account:login'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'account/login.html')
        self.assertTrue('title' in response.context)
        self.assertTrue(response.context['title'] == 'Авторизация')

    def test_user_login_redirect_success(self):
        self.client.post(reverse('account:register'), self.data)
        self.client.login(username=self.data['username'], password=self.data['password1'])
        response = self.client.get(reverse('account:login'))
        # проверка перенаправления на главную страницу, если пользователь уже залогинился
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('index'))


class ProfileUserViewTest(TestCase):
    def setUp(self):
        user1 = get_user_model().objects.create_user(username='test_user', password='12345')
        self.user = user1

        for post_num in range(3):
            Post.objects.create(title='Title %s' % post_num,
                                slug='title_one_%s' % post_num,
                                body='Title_one_text %s' % post_num,
                                author=user1,
                                status='PB')

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('account:profile', args=(self.user.pk,)))
        self.assertRedirects(resp, f'/account/login/?next=/account/profile/{self.user.pk}/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='test_user', password='12345')
        resp = self.client.get(reverse('account:profile', args=(self.user.pk,)))

        # Проверка, что пользователь залогинился
        self.assertEqual(str(resp.context['user']), 'test_user')

        # Проверка ответа на запрос
        self.assertEqual(resp.status_code, HTTPStatus.OK)

        # Проверка использования правильного шаблона
        self.assertTemplateUsed(resp, 'account/profile.html')

    def test_title(self):
        login = self.client.login(username='test_user', password='12345')
        response = self.client.get(reverse('account:profile', args=(self.user.pk,)))
        self.assertTrue('title' in response.context)
        self.assertTrue(response.context['title'] == f'Профиль: {self.user.username}')

    def test_profile_content(self):
        login = self.client.login(username='test_user', password='12345')
        response = self.client.get(reverse('account:profile', args=(self.user.pk,)))
        posts = Post.objects.filter(author__username='test_user')
        self.assertQuerysetEqual(posts, response.context_data['username_posts'])


class EditProfileUserViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test_user', password='12345')

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('account:edit_profile'))
        self.assertRedirects(resp, f'/account/login/?next=/account/edit_profile/')

    def test_uses_correct_template(self):
        login = self.client.login(username='test_user', password='12345')
        resp = self.client.get(reverse('account:edit_profile'))
        self.assertEqual(resp.status_code, HTTPStatus.OK)

        # Проверка использования корректного шаблона
        self.assertTemplateUsed(resp, 'account/edit_profile.html')

    def test_title(self):
        login = self.client.login(username='test_user', password='12345')
        response = self.client.get(reverse('account:edit_profile'))
        self.assertTrue('title' in response.context)
        self.assertTrue(response.context['title'] == 'Профиль пользователя')

    def test_redirects_to_profile_page_on_success(self):
        # После успешного редактирования профиля происходит перенаправление на обновленный профиль пользователя
        login = self.client.login(username='test_user', password='12345')
        resp = self.client.post(reverse('account:edit_profile'),
                                {'first_name': 'Имя'},
                                follow=True)
        self.assertTrue(resp, self.user.get_absolute_url())


class UserPasswordChangeViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test_user', password='12345')

    def test_uses_correct_template(self):
        login = self.client.login(username='test_user', password='12345')
        resp = self.client.get(reverse('account:password_change'))
        self.assertEqual(resp.status_code, HTTPStatus.OK)

        # Проверка использования корректного шаблона
        self.assertTemplateUsed(resp, 'account/password_change_form.html')

    def test_title(self):
        login = self.client.login(username='test_user', password='12345')
        response = self.client.get(reverse('account:password_change'))
        self.assertTrue('title' in response.context)
        self.assertTrue(response.context['title'] == 'Изменение пароля')

    def test_redirects_to_main_page_on_success(self):
        # После успешного изменения пароля происходит перенаправление на страницу,
        # подтверждающую успешное изменение пароля
        login = self.client.login(username='test_user', password='12345')
        resp = self.client.post(reverse('account:password_change'),
                                {'old_password': '12345',
                                 'new_password1': '12345678Aa',
                                 'new_password2': '12345678Aa'},
                                follow=True)
        self.assertTrue(resp, reverse('account:password_change_done'))


class CreateUserFollowingViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test_user1', password='12345')
        self.follower = get_user_model().objects.create_user(username='test_user2', password='12345')

    def test_follow_not_logged_in(self):
        response = self.client.post(reverse('account:follow', args=(self.user.pk,)))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_follow_logged_in(self):
        user_followers_before = self.user.followers.all()
        self.assertTrue(self.follower not in user_followers_before)
        login = self.client.login(username='test_user2', password='12345')
        response = self.client.post(reverse('account:follow', args=(self.user.pk,)))
        user_followers_after = self.user.followers.all()
        self.assertTrue(self.follower in user_followers_after)
        self.assertRedirects(response, reverse('account:profile', args=(self.user.pk,)))
