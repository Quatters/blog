# Блог

Данный проект - выполненное тестовое задание на позицию Junior Fullstack Developer.

## Что сделано?

Основное:

- [x] Регистрация, token-аутентификация
- [x] Просмотр списка постов
- [x] Просмотр отдельного поста с комментариями
- [x] Возможность создать пост
- [x] Возможность написать комментарий к посту

Дополнительно:

- [x] Пагинация постов и комментариев (infinite scroll)
- [x] Тесты для всех endpoint'ов (backend)

## Запуск в Docker

Перед запуском `docker-compose` переименуйте файл `server/example.env` в `server/.env` и по крайней мере измените значение `SECRET_KEY`.

Затем примените миграции:

```
docker compose up db -d && docker-compose run backend python manage.py migrate
```

Наконец, поднимите контейнеры:

```
docker-compose up
```

Сервер клиента будет доступен по адресу [localhost:3000](http://localhost:3000), backend-сервер - на [localhost:8000](http://localhost:8000).

Также можно запустить тесты с помощью

```
docker-compose run backend python manage.py test
```

## Техническая информация

Backend обслуживает следующие маршруты:

- /api/posts/
  - GET - список постов, поддерживаются query-параметры limit, offset
  - POST { title, body } - создать пост (необходим HTTP заголовок Authorization: Token &lt;token&gt;)
- /api/posts/:id/
  - GET - пост с указанным id
- /api/comments/:post_id/
  - GET - список комментариев для поста с id = post_id, поддерживаются query-параметры limit, offset
  - POST { body } - создать комментарий для поста с id = post_id (необходим HTTP заголовок Authorization: Token &lt;token&gt;)
- /api/auth/login/
  - POST { username, password } - получить токен авторизации
- /api/auth/register/
  - POST { username, password, repeat_password } - зарегистрировать пользователя
- /api/auth/user/
  - GET - получить username текущего пользователя (необходим HTTP заголовок Authorization: Token &lt;token&gt;)
