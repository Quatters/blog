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

## Запуск dev-сервера

Выполните `./manage.py runserver` в директории `server/`.

Перед запуском клиентского dev-сервера установите зависимости: `npm install` в директории `client/`,

затем запустите его с помощью `npm run dev`.

## Техническая информация

При разработке backend'а использовался **Python v3.10** вместе с **Django v3.2**. БД - дефолтная **SQLite**, файл сгенерирован Django.

Для frontend'а использовались **Node v16.13**, **npm v8.5**.

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
