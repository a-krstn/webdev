from django.core.mail import send_mail
from django.db.models import Count
from datetime import datetime, timedelta
import os

from celery import shared_task

from account.models import User
from .models import Post


@shared_task
def post_created(post_slug: str) -> None:
    """
    Задача, уведомляющая по почте подписчика о публикации нового поста автора
    """

    post = Post.objects.get(slug=post_slug)
    subject = f'Новый пост'
    message = f'Пользователь {post.author} опубликовал новую статью.\n' \
              f'Читать http://webdev.com{post.get_absolute_url()}'
    for follower in post.author.followers.all():
        send_mail(subject,
                  message,
                  os.getenv('EMAIL_HOST_USER'),
                  [follower.email])


@shared_task()
def send_beat_email() -> None:
    """
    Периодическая задача, отправляющая раз в неделю всем пользователям
    3 самых обсуждаемых поста за прошедший период
    """

    date_week_ago = datetime.now() - timedelta(days=7)

    # Запрос трех наиболее обсуждаемых постов за прошедшую неделю
    most_commented_posts = Post.published.filter(publish__gt=date_week_ago) \
                               .annotate(num_comments=Count('comments')) \
                               .order_by('-num_comments')[:3]

    # Формирование списка в формате post.title: link
    posts_in_title_link_format = [f'{post.title}: http://webdev.com{post.get_absolute_url()}\n'
                                  for post in most_commented_posts]

    message = f'Самые обсуждаемые посты прошедшей недели:\n' \
              f'{''.join(posts_in_title_link_format)}'

    for user in User.objects.all():
        send_mail(
            'Возможно, Вам будет это интересно',
            message,
            os.getenv('EMAIL_HOST_USER'),
            [user.email]
        )

