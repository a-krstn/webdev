#!/bin/sh

./wait-for-it.sh db:5432
cd webdev
python manage.py makemigrations
python manage.py migrate
python manage.py fill_db
python manage.py collectstatic --no-input
python manage.py shell -c "from account.models import User; User.objects.create_superuser('admin', 'al-krstn@yandex.ru', '12345')"
gunicorn --workers=2 webdev.wsgi:application --bind 0.0.0.0:8000