import random

from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

from post.models import Post, Category, Comment, Tag
from account.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        Post.objects.all().delete()
        Category.objects.all().delete()
        Comment.objects.all().delete()
        Tag.objects.all().delete()
        User.objects.all().delete()
        Group.objects.all().delete()

        # Создание группы "Пользователи" и добавление разрешений в группу
        general_group = Group.objects.create(name='Пользователи')
        permission_codenames = ('add_post', 'change_post', 'delete_post', 'view_post',
                                'add_comment', 'change_comment', 'delete_comment', 'view_comment')
        permission_objects = [Permission.objects.get(codename=code_name) for code_name in permission_codenames]
        general_group.permissions.set(permission_objects)

        # Создание 10 юзеров
        users = [User(username=f'User{i}', email=f'user{i}@mail.ru', password='12345') for i in range(1, 11)]
        User.objects.bulk_create(users)
        for user in users:
            user.groups.add(general_group)

        users_ids_list = list(User.objects.values_list('id', flat=True))

        # Создание 10 категорий
        categories = [Category(cat_title=f'Категория{i}', slug=f'category{i}') for i in range(1, 11)]
        Category.objects.bulk_create(categories)

        cats_ids_list = list(Category.objects.values_list('id', flat=True))

        # Создание 20 тегов
        tags = [Tag(name=f'тэг{i}', slug=f'tag{i}') for i in range(1, 21)]
        Tag.objects.bulk_create(tags)

        tags_ids_list = list(Tag.objects.values_list('id', flat=True))

        # Создание 100 постов
        post_template = {
            'body': '''<p>Текст этого поста является шаблоном и служит лишь для создания тестовых данных в БД.
                    Текст этого поста является шаблоном и служит лишь для создания тестовых данных в БД.
                    Текст этого поста является шаблоном и служит лишь для создания тестовых данных в БД.
                    Текст этого поста является шаблоном и служит лишь для создания тестовых данных в БД.</p>''',
            'title_image': None,
        }

        posts = [Post(title=f'Заголовок{i}',
                      slug=f'zagolovok{i}',
                      author_id=random.choice(users_ids_list),
                      **post_template) for i in range(1, 101)]
        Post.objects.bulk_create(posts)

        posts_ids_list = list(Post.objects.values_list('id', flat=True))

        # Создание 200 комментов
        comment_template = {
            'body': '''Комментарий к посту''',
        }

        comments = [Comment(post_id=random.choice(posts_ids_list),
                            author_id=random.choice(users_ids_list),
                            **comment_template) for _ in range(1, 201)]
        Comment.objects.bulk_create(comments)

        # Присваивание каждому посту категории и нескольких тегов
        for post in Post.objects.all():
            post.cat_id = random.choice(cats_ids_list)
            random_tag_ids = random.sample(tags_ids_list, random.randint(1, 5))
            post.tags.set(random_tag_ids)
            post.save()

