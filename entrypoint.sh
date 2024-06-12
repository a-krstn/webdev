#!/bin/sh

cd webdev
python manage.py makemigrations
python manage.py migrate
python manage.py fill_db
python manage.py collectstatic --no-input
gunicorn --workers=2 webdev.wsgi:application --bind 0.0.0.0:8000