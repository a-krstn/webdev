from django.contrib.auth.models import Group
from django.db.models import Manager, QuerySet
from django.shortcuts import get_object_or_404

from slugify import slugify

# from api.serializers import TagListSerializer
from post.forms import PostForm, CommentForm
from post.tasks import *


def only_objects_decorator(func: callable) -> callable:
    """Позволяет функциям, обращающимся к БД, принимать параметр only"""

    def only_objects_wrapper(objects: Manager, only=(), *args, **kwargs):
        return func(objects, *args, **kwargs).only(*only)

    return only_objects_wrapper


def select_related_objects_decorator(func: callable) -> callable:
    """Позволяет функциям, обращающимся к БД, принимать параметр select_related"""

    def select_related_objects_wrapper(objects, select_related=(), *args, **kwargs):
        return func(objects, *args, **kwargs).select_related(*select_related)

    return select_related_objects_wrapper


def prefetch_related_objects_decorator(func: callable) -> callable:
    """Позволяет функциям, обращающимся к БД, принимать параметр prefetch_related"""

    def prefetch_related_objects_wrapper(objects, prefetch_related=(), *args, **kwargs):
        return func(objects, *args, **kwargs).prefetch_related(*prefetch_related)

    return prefetch_related_objects_wrapper


@only_objects_decorator
@prefetch_related_objects_decorator
@select_related_objects_decorator
def all_objects(objects: Manager, count: int = None) -> QuerySet:
    """Возвращает все объекты"""

    if count is None:
        return objects.all()
    return objects.all()


@only_objects_decorator
@prefetch_related_objects_decorator
@select_related_objects_decorator
def filter_objects(objects: Manager, **kwargs) -> QuerySet:
    """Возвращает отфильтрованные объекты"""

    return objects.filter(**kwargs)


def get_instance_by_unique_field(model, **kwargs):
    """Возвращает объект из БД по уникальному полю"""

    return get_object_or_404(model, **kwargs)


def create_post(form: PostForm, user: User) -> None:
    """Создает объект модели Post"""

    post = form.save(commit=False)
    post.author = user
    post.slug = slugify(post.title)
    post.save()
    post.tags.set(form.cleaned_data['tags'])
    post_created.delay(post.slug)


def create_comment(form: CommentForm, user, post) -> None:
    """Создает объект модели Comment"""

    comment = form.save(commit=False)
    comment.author = user
    comment.post_id = post.pk
    comment.save()


def create_user(form) -> None:
    """Создает объект модели User"""

    user = form.save()
    group = Group.objects.get(name='Пользователи')
    user.groups.add(group)


def create_tag_serializer(serializer, name: str) -> None:
    """Создает объект класса Tag"""

    serializer.save(slug=slugify(name))


def subscribe(user: User, follower: User) -> bool:
    """Осуществляет подписку follower на user"""

    if follower in user.followers.all():
        user.followers.remove(follower)
        return True
    user.followers.add(follower)
    return False
