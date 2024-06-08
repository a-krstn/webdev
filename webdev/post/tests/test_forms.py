from django.test import TestCase

from post.forms import SearchForm


class PostFormTest(TestCase):
    def test_query_field_label(self):
        form = SearchForm()
        self.assertTrue(form.fields['query'].label == 'Введите запрос')
