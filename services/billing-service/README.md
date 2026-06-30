# billing-service

Отвечает за счета пользователей и операции с балансом.

## Задачи

- Создать счет пользователя.
- Пополнить счет.
- Списать деньги.
- Получить баланс.

## Правила

- У пользователя один счет.
- Баланс не может быть отрицательным.
- Если денег не хватает, списание не выполняется.

## Минимальное API

```http
POST /accounts
GET /accounts/{userId}
POST /accounts/{userId}/deposit
POST /accounts/{userId}/withdraw
```

## TODO

- Описать модели request/response.
- Описать SQLAlchemy model для account.
- Реализовать операции с балансом.
- Подключить миграции.
- Добавить Kubernetes/Helm values.
