from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from . import serializers
from api.serializers import CategoryDetailSerializer, TagDetailSerializer, UserDetailSerializer, \
    CommentDetailSerializer, PostDetailSerializer
from post.models import Post, Category, Tag, Comment


class CategoryListTest(APITestCase):
    def setUp(self):
        for i in range(1, 7):
            Category.objects.create(cat_title=f'Category {i}',
                                    slug=f'category_{i}')

        self.user = get_user_model().objects.create_user(username='test_user1',
                                                         password='12345')
        self.super_user = get_user_model().objects.create_user(username='test_user2',
                                                               password='12345',
                                                               is_superuser=True)

        self.user_token = Token.objects.create(user=self.user)
        self.super_user_token = Token.objects.create(user=self.super_user)

    def test_cat_list(self):
        response = self.client.get(reverse('api:category-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # проверка кол-ва записей на одной странице
        self.assertEqual(len(response.data['results']), 5)

    def test_cat_list_next_page(self):
        response = self.client.get(reverse('api:category-list') + '?offset=5')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_new_cat_not_logged(self):
        data = {'cat_title': 'Category 7', 'slug': 'category_7'}
        response = self.client.post(reverse('api:category-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_new_cat_logged_not_superuser(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        data = {'cat_title': 'Category 7', 'slug': 'category_7'}
        response = self.client.post(reverse('api:category-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_new_cat_logged_and_superuser(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.super_user_token.key)
        data = {'cat_title': 'Category 7', 'slug': 'category_7'}
        response = self.client.post(reverse('api:category-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class CategoryDetailTest(APITestCase):
    def setUp(self):
        # perm = Permission.objects.get(name='Can change Категория')

        self.cat = Category.objects.create(cat_title='Category 1',
                                           slug='category_1')
        self.cat.save()

        self.user = get_user_model().objects.create_user(username='test_user1',
                                                         password='12345')
        self.super_user = get_user_model().objects.create_user(username='test_user2',
                                                               password='12345',
                                                               is_superuser=True)

        self.user_token = Token.objects.create(user=self.user)
        self.super_user_token = Token.objects.create(user=self.super_user)

    def test_cat_detail(self):
        response = self.client.get(reverse('api:category-detail', args=(self.cat.pk,)))
        serializer_data = serializers.CategoryDetailSerializer(self.cat).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('cat_title'), "Category 1")
        self.assertEqual(serializer_data, response.data)

    def test_cat_update_not_logged(self):
        data = {'cat_title': 'Category 5'}
        response = self.client.put(reverse('api:category-detail', args=(self.cat.pk,)), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cat_update_logged_not_superuser(self):
        data = {'cat_title': 'Category 5'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        response = self.client.put(reverse('api:category-detail', args=(self.cat.pk,)), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cat_update_logged_superuser(self):
        data = {'cat_title': 'Category 5'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.super_user_token.key)
        response = self.client.put(reverse('api:category-detail', args=(self.cat.pk,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cat_delete_not_logged(self):
        response = self.client.delete(reverse('api:category-detail', args=(self.cat.pk,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cat_delete_logged_not_superuser(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        response = self.client.delete(reverse('api:category-detail', args=(self.cat.pk,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cat_delete_logged_superuser(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.super_user_token.key)
        response = self.client.delete(reverse('api:category-detail', args=(self.cat.pk,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TagListTest(APITestCase):
    def setUp(self):
        for i in range(1, 7):
            Tag.objects.create(name=f'Tag {i}',
                               slug=f'tag_{i}')

        self.user = get_user_model().objects.create_user(username='test_user1',
                                                         password='12345')

        self.user_token = Token.objects.create(user=self.user)

    def test_tag_list(self):
        response = self.client.get(reverse('api:tag-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # проверка кол-ва записей на одной странице
        self.assertEqual(len(response.data['results']), 5)

    def test_tag_list_next_page(self):
        response = self.client.get(reverse('api:tag-list') + '?offset=5')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_new_tag_not_logged(self):
        data = {'name': 'Tag 7', 'slug': 'tag_7'}
        response = self.client.post(reverse('api:tag-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_new_tag_logged(self):
        data = {'name': 'Tag 7', 'slug': 'tag_7'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        response = self.client.post(reverse('api:tag-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TagDetailTest(APITestCase):
    def setUp(self):
        self.tag = Tag.objects.create(name='Tag 1',
                                      slug='tag_1')
        self.tag.save()

        self.user = get_user_model().objects.create_user(username='test_user1',
                                                         password='12345')
        self.super_user = get_user_model().objects.create_user(username='test_user2',
                                                               password='12345',
                                                               is_superuser=True)

        self.user_token = Token.objects.create(user=self.user)
        self.super_user_token = Token.objects.create(user=self.super_user)

    def test_tag_detail(self):
        response = self.client.get(reverse('api:tag-detail', args=(self.tag.pk,)))
        serializer_data = serializers.TagDetailSerializer(self.tag).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('name'), "Tag 1")
        self.assertEqual(serializer_data, response.data)

    def test_tag_update_not_logged(self):
        data = {'name': 'Tag 5'}
        response = self.client.put(reverse('api:tag-detail', args=(self.tag.pk,)), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_tag_update_logged_not_superuser(self):
        data = {'name': 'Tag 5'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        response = self.client.put(reverse('api:tag-detail', args=(self.tag.pk,)), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_tag_update_logged_superuser(self):
        data = {'name': 'Tag 5'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.super_user_token.key)
        response = self.client.put(reverse('api:tag-detail', args=(self.tag.pk,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_tag_delete_not_logged(self):
        response = self.client.delete(reverse('api:tag-detail', args=(self.tag.pk,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_tag_delete_logged_not_superuser(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        response = self.client.delete(reverse('api:tag-detail', args=(self.tag.pk,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_tag_delete_logged_superuser(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.super_user_token.key)
        response = self.client.delete(reverse('api:tag-detail', args=(self.tag.pk,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class UserListTest(APITestCase):
    def setUp(self):
        for i in range(1, 7):
            get_user_model().objects.create(username=f'User {i}',
                                            email=f'user{i}@mail.ru',
                                            password='12345')

        self.user = get_user_model().objects.create_user(username='test_user1',
                                                         password='12345')

        self.user_token = Token.objects.create(user=self.user)

    def test_user_list_not_logged(self):
        response = self.client.get(reverse('api:user-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_list_logged(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        response = self.client.get(reverse('api:user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # проверка кол-ва записей на одной странице
        self.assertEqual(len(response.data['results']), 5)

    def test_user_list_logged_next_page(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        response = self.client.get(reverse('api:user-list') + '?offset=5')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_create_new_user_not_logged(self):
        data = {'username': 'User 1', 'email': 'user1@mail.ru', 'password1': '12345', 'password2': '12345'}
        response = self.client.post(reverse('api:user-list'), data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_create_new_user_logged(self):
        data = {'username': 'User 1', 'email': 'user1@mail.ru', 'password1': '12345', 'password2': '12345'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        response = self.client.post(reverse('api:user-list'), data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class UserDetailTest(APITestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(username='test_user1',
                                                          password='12345')
        self.user2 = get_user_model().objects.create_user(username='test_user2',
                                                          password='12345')

        self.user1_token = Token.objects.create(user=self.user1)
        self.user2_token = Token.objects.create(user=self.user2)

    def test_user_detail(self):
        response = self.client.get(reverse('api:user-detail', args=(self.user1.pk,)))
        serializer_data = serializers.UserDetailSerializer(self.user1).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('username'), "test_user1")
        # ссылка на дефолтную картинку разная
        # self.assertEqual(serializer_data, response.data)

    def test_user_update_not_logged(self):
        data = {'first_name': 'Name'}
        response = self.client.put(reverse('api:user-detail', args=(self.user1.pk,)), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_update_logged_not_owner(self):
        data = {'first_name': 'Name'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user2_token.key)
        response = self.client.put(reverse('api:user-detail', args=(self.user1.pk,)), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_update_logged_owner(self):
        data = {'first_name': 'Name'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.put(reverse('api:user-detail', args=(self.user1.pk,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_delete_not_logged(self):
        response = self.client.delete(reverse('api:user-detail', args=(self.user1.pk,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_delete_logged_not_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user2_token.key)
        response = self.client.delete(reverse('api:user-detail', args=(self.user1.pk,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_delete_logged_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.delete(reverse('api:user-detail', args=(self.user1.pk,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class CommentListTest(APITestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(username='test_user1',
                                                          password='12345')

        self.user1_token = Token.objects.create(user=self.user1)

        category = Category.objects.create(cat_title='Category 1',
                                           slug='category_1')

        self.post = Post.objects.create(title='Post title',
                                        slug='post_title',
                                        cat=category,
                                        author=self.user1,
                                        body='Post text')

        for i in range(1, 7):
            Comment.objects.create(body=f'Comment {i} on post',
                                   author=self.user1,
                                   post=self.post)

    def test_comment_list(self):
        response = self.client.get(reverse('api:comment-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # проверка кол-ва записей на одной странице
        self.assertEqual(len(response.data['results']), 5)

    def test_comment_list_next_page(self):
        response = self.client.get(reverse('api:comment-list') + '?offset=5')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_new_comment_not_logged(self):
        data = {'body': 'New comment to post', 'post': self.post}
        response = self.client.post(reverse('api:comment-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_new_comment_logged(self):
        data = {'body': 'New comment to post', 'post': self.post}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.post(reverse('api:comment-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class CommentDetailTest(APITestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(username='test_user1',
                                                          password='12345')
        self.user2 = get_user_model().objects.create_user(username='test_user2',
                                                          password='12345')

        self.user1_token = Token.objects.create(user=self.user1)
        self.user2_token = Token.objects.create(user=self.user2)

        category = Category.objects.create(cat_title='Category 1',
                                           slug='category_1')

        self.post = Post.objects.create(title='Post title',
                                        slug='post_title',
                                        cat=category,
                                        author=self.user1,
                                        body='Post text')

        self.comment = Comment.objects.create(body='Comment to post',
                                              post=self.post,
                                              author=self.user1)

    def test_comment_detail(self):
        response = self.client.get(reverse('api:comment-detail', args=(self.comment.pk,)))
        serializer_data = CommentDetailSerializer(self.comment).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('body'), "Comment to post")
        self.assertEqual(serializer_data, response.data)

    def test_comment_update_not_logged(self):
        data = {'body': 'Updated comment to post'}
        response = self.client.put(reverse('api:comment-detail', args=(self.comment.pk,)), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_comment_update_logged_not_owner(self):
        data = {'body': 'Updated comment to post'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user2_token.key)
        response = self.client.put(reverse('api:comment-detail', args=(self.comment.pk,)), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_comment_update_logged_owner(self):
        data = {'body': 'Updated comment to post',
                'post': self.post.pk}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.put(reverse('api:comment-detail', args=(self.comment.pk,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_comment_delete_not_logged(self):
        response = self.client.delete(reverse('api:comment-detail', args=(self.comment.pk,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_comment_delete_logged_not_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user2_token.key)
        response = self.client.delete(reverse('api:comment-detail', args=(self.comment.pk,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_comment_delete_logged_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.delete(reverse('api:comment-detail', args=(self.comment.pk,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class PostViewSetTest(APITestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(username='test_user1',
                                                          password='12345')
        self.user2 = get_user_model().objects.create_user(username='test_user2',
                                                          password='12345')

        self.user1_token = Token.objects.create(user=self.user1)
        self.user2_token = Token.objects.create(user=self.user2)

        self.category = Category.objects.create(cat_title='Category 1',
                                                slug='category_1')

        for i in range(1, 7):
            Post.objects.create(title=f'Post title {i}',
                                slug=f'post_title_{i}',
                                cat=self.category,
                                body='Post text',
                                author=self.user1)

        self.post = Post.objects.last()

    def test_post_list(self):
        response = self.client.get(reverse('api:post-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # проверка кол-ва записей на одной странице
        self.assertEqual(len(response.data['results']), 5)

    def test_post_list_next_page(self):
        response = self.client.get(reverse('api:post-list') + '?offset=5')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_new_post_not_logged(self):
        data = {
            'title': 'Post title 10',
            'slug': 'post_title_10',
            'cat': self.category,
            'author': self.user1,
            'body': 'New comment to post',
            }
        response = self.client.post(reverse('api:post-list'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_new_post_logged(self):
        data = {
            'title': 'Post title 8',
            'slug': 'post_title_8',
            'cat': self.category.pk,
            'author': self.user1,
            'body': 'New post text',
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.post(reverse('api:post-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_detail(self):
        response = self.client.get(reverse('api:post-detail', args=(self.post.pk,)))
        serializer_data = PostDetailSerializer(self.post).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('title'), self.post.title)
        self.assertEqual(serializer_data, response.data)

    def test_post_update_not_logged(self):
        data = {'body': 'Updated text in post'}
        response = self.client.put(reverse('api:post-detail', args=(self.post.pk,)), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_update_logged_not_owner(self):
        data = {'body': 'Updated text in post'}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user2_token.key)
        response = self.client.put(reverse('api:post-detail', args=(self.post.pk,)), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_update_logged_owner(self):
        data = {'title': 'Updated post title',
                'body': 'Updated text in post',
                'post': self.post.pk}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.put(reverse('api:post-detail', args=(self.post.pk,)), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_delete_not_logged(self):
        response = self.client.delete(reverse('api:post-detail', args=(self.post.pk,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_delete_logged_not_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user2_token.key)
        response = self.client.delete(reverse('api:post-detail', args=(self.post.pk,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_delete_logged_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user1_token.key)
        response = self.client.delete(reverse('api:post-detail', args=(self.post.pk,)))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class CreateUserFollowingTest(APITestCase):
    def setUp(self):
        self.user1 = get_user_model().objects.create_user(username='test_user1',
                                                          password='12345')
        self.user2 = get_user_model().objects.create_user(username='test_user2',
                                                          password='12345')

        self.user1_token = Token.objects.create(user=self.user1)
        self.user2_token = Token.objects.create(user=self.user2)

    def test_follow_not_logged(self):
        response = self.client.post(reverse('api:follow', args=(self.user1.pk,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_follow_logged(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user2_token.key)
        response = self.client.post(reverse('api:follow', args=(self.user1.pk,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user1 in self.user2.following.all())
