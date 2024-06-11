# Webdev.com

## Содержание
- [О проекте](#о-проекте)
- [Стек](#стек)
- [Начало работы](#начало-работы)
- [Эндпоинты API](#эндпоинты-api)
- [Тестирование](#тестирование)
- [Лицензия](#лицензия)

## О проекте
Приложение представляет собой тематический коллективный блог с элементами новостного сайта.
В нем реализованы:
- система постов
- система комментариев
- система аккаунтов
- система подписок
- сортировка постов по категориям и тегам
- отправка уведомлений на почту о выходе новых постов/самых обсуждаемых постов за определенный период
- RESTful API приложения

## Стек
- Django
- Django REST framework
- PostgreSQL
- Redis
- Celery/Celery Beat
- Flower
- HTML/CSS/Bootstrap

## Начало работы
1. **Клонирование приложения**<br>
   `git clone git@github.com:a-krstn/webdev.git`
2. **Создание виртуального окружения и его активация**<br>
   В командной строке из директории проекта<br>
   `python -m venv .venv`<br>
   - Windows: `.venv\Scripts\activate`<br>
   - Linux/MacOS: `source .venv/bin/activate`
3. **Установка зависимостей**<br>
   `pip install -r webdev/requirements.txt`
4. **Определение переменных среды**<br>
   Для успешного запуска приложения требуется создать файл .env
   в корневой папке проекта и определить в нем переменные среды. Перечень требуемых переменных
   перечислен в файле .env.example.
5. **Запуск приложения**<br>
   (**Важно:** для успешного запуска приложения локально необходим
   развернутый сервер Redis на порту 6379)<br>
   Локально: `python manage.py runserver --settings=webdev.settings.local`<br>
   В docker: `docker compose up`<br>
   Приложение будет доступно по адресу `http://127.0.0.1:8000/`

## Эндпоинты API
Документация API приложения доступна после запуска приложения
по адресам:
- http://127.0.0.1:8000/swagger/
- http://127.0.0.1:8000/redoc/

## Тестирование
Для тестирования приложения используются юнит-тесты.<br>
Для запуска всех тестов:<br>
(**Важно:** для успешного запуска тестов необходимо, чтобы действия 1-3
[Начало работы](#начало-работы) были выполнены, а также был развернут
сервер Redis на порту 6379)<br>
`python manage.py test . --settings=webdev.settings.local`

## Лицензия
MIT License
