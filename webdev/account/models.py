from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.conf import settings

from easy_thumbnails.fields import ThumbnailerImageField


class User(AbstractUser):
    photo = ThumbnailerImageField(upload_to='account/%Y/%m/%d/',
                                  blank=True,
                                  null=True,
                                  verbose_name='Изображение',
                                  default=settings.DEFAULT_USER_IMAGE,
                                  resize_source=dict(quality=98,
                                                     size=(64, 64),
                                                     sharpen=True))
    following = models.ManyToManyField('self',
                                       related_name='followers',
                                       symmetrical=False,
                                       blank=True,
                                       verbose_name='Подписки')

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('account:profile', args=[self.pk])
