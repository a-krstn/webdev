from .base import *

DEBUG = True
ADMINS = [
    ('Admin', os.getenv('EMAIL_HOST_USER')),
]

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': 5432,
    }
}

REDIS_URL = 'redis://cache:6379'
REDIS_HOST = 'cache'
REDIS_PORT = 6379
CACHES['default']['LOCATION'] = REDIS_URL

CELERY_BROKER_URL = 'redis://' + REDIS_HOST + ':' + str(REDIS_PORT) + '/0'
CELERY_RESULT_BACKEND = 'redis://' + REDIS_HOST + ':' + str(REDIS_PORT) + '/0'
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_ACCEPT_BACKEND = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT = True
