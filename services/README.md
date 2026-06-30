# Services

Здесь лежат заготовки микросервисов для ДЗ.

Рекомендуемый состав:

- `user-service`
- `billing-service`
- `order-service`
- `notification-service`

Каждый сервис можно реализовать независимо: свой Dockerfile, свои зависимости, своя БД или схема БД.

Базовая структура сервиса:

```text
service-name/
  Dockerfile
  main.py
  pyproject.toml
  requirements.txt
  src/
    app/
      api/v1/
      core/
      db/
      modules/
    alembic/versions/
    tests/
      api/
      integration/
```

В новых сервисах `main.py` и Dockerfile оставлены как заготовки: бизнес-логику нужно добавить при реализации.
