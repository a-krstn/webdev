from django.contrib.auth import get_user_model
from django.test import TestCase


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        get_user_model().objects.create(username='user')

    def test_photo_label(self):
        user = get_user_model().objects.last()
        field_label = user._meta.get_field('photo').verbose_name
        self.assertEqual(field_label, 'Изображение')

    def test_following_label(self):
        user = get_user_model().objects.last()
        field_label = user._meta.get_field('following').verbose_name
        self.assertEqual(field_label, 'Подписки')

    def test_object_name_is_username(self):
        user = get_user_model().objects.last()
        expected_object_name = user.username
        self.assertEqual(expected_object_name, str(user))

    def test_get_absolute_url(self):
        user = get_user_model().objects.last()
        self.assertEqual(user.get_absolute_url(), f'/account/profile/{user.pk}/')
