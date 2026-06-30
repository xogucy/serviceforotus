# user-service

Отвечает за пользователей.

Текущий FastAPI-код перенесен сюда из корневой папки проекта.

## Задачи

- Создать пользователя.
- Получить пользователя.
- При создании пользователя вызвать billing-service и создать счет.

## Минимальное API

```http
POST /users
GET /users/{userId}
```

## Интеграции

```text
user-service -> billing-service: POST /accounts
```

## TODO

- Описать модели request/response.
- Реализовать HTTP API.
- Добавить Kubernetes/Helm values.
