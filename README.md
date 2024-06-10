# Webdev.com

## Содержание
- [О проекте](#о проекте)
- [Стек](#стек)
- [Начало работы](#начало-работы)
- [Тестирование](#тестирование)

## О проекте
Приложение представляет собой тематический коллективный блог с элементами новостного сайта.

## Стек
- Django
- Django REST framework
- PostgreSQL
- Redis
- Celery/Celery Beat
- Flower
- HTML/CSS/Bootstrap

## Начало работы
1. **Клонирование приложения**\
   `git clone git@github.com:a-krstn/webdev.git`
2. **Создание виртуального окружения и его активация**\
   В командной строке в директории проекта\
   `python -m venv .venv`\
   `.venv\Scripts\activate`
3. **Установка зависимостей**\
   `pip install -r webdev/requirements.txt`
4. **Запуск приложения**\
   Локально: `python manage.py runserver --settings=webdev.settings.local`\
   Через docker: `docker compose up` (`http://webdev.com`)

## Тестирование
Для тестирования приложения используются юнит-тесты.\
Для запуска тестов выполнить действия пп. 1-3 [Начало работы](#начало-работы), затем\
`python manage.py test . --settings=webdev.settings.local`

