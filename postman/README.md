# Postman/Newman

Здесь будут Postman collection и environment для проверки ДЗ.

## Environment

Обязательная переменная:

```text
baseUrl = http://arch.homework
```

## Сценарий

1. Создать пользователя.
2. Проверить, что account создан в billing-service.
3. Пополнить счет.
4. Создать успешный заказ.
5. Проверить, что баланс уменьшился.
6. Проверить успешное уведомление.
7. Создать неуспешный заказ.
8. Проверить, что баланс не изменился.
9. Проверить неуспешное уведомление.

## Запуск

```bash
newman run postman/orders-homework.postman_collection.json \
  -e postman/orders-homework.postman_environment.json \
  --reporters cli
```

