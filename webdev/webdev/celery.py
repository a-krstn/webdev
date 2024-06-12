import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# создание переменной окружения для командной строки Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webdev.settings.local')

# создание экземпляра приложения
app = Celery('webdev')

# загрузка конфига из настроек проекта
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.timezone = 'Europe/Moscow'

# Автообнаружение асинхронных заданий в приложениях
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'send-email-every-week': {
        'task': 'post.tasks.send_beat_email',
        'schedule': crontab(minute='0',
                            hour='9',
                            day_of_week='saturday'),
    },
}
