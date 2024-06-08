from django.contrib.auth import get_user_model
from django.test import TestCase

from account.forms import LoginForm, UserRegistrationForm, ProfileUserForm, UserPasswordChangeForm


class LoginFormTest(TestCase):
    def test_username_field_label(self):
        form = LoginForm()
        self.assertTrue(form.fields['username'].label == 'Email')

    def test_password_field_label(self):
        form = LoginForm()
        self.assertTrue(form.fields['password'].label == 'Пароль')


class RegistrationFormTest(TestCase):
    def test_password1_field_label(self):
        form = UserRegistrationForm()
        self.assertTrue(form.fields['password1'].label == 'Пароль')

    def test_password2_field_label(self):
        form = UserRegistrationForm()
        self.assertTrue(form.fields['password2'].label == 'Повторите пароль')


class ProfileUserFormTest(TestCase):
    def test_username_field_label(self):
        form = ProfileUserForm()
        self.assertTrue(form.fields['username'].label == 'Имя пользователя')

    def test_email_field_label(self):
        form = ProfileUserForm()
        self.assertTrue(form.fields['email'].label == 'Email')


class UserPasswordChangeFormTest(TestCase):
    def test_old_password_field_label(self):
        form = UserPasswordChangeForm(get_user_model().objects.create(username='admin'))
        self.assertTrue(form.fields['old_password'].label == 'Старый пароль')

    def test_new_password1_field_label(self):
        form = UserPasswordChangeForm(get_user_model().objects.create(username='admin'))
        self.assertTrue(form.fields['new_password1'].label == 'Новый пароль')

    def test_new_password2_field_label(self):
        form = UserPasswordChangeForm(get_user_model().objects.create(username='admin'))
        self.assertTrue(form.fields['new_password2'].label == 'Повторите новый пароль')
