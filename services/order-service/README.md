# order-service

Отвечает за создание заказов.

## Задачи

- Принять заказ с `userId`, `email`, `price`.
- Вызвать billing-service для списания денег.
- Сохранить заказ со статусом оплаты.
- Опубликовать событие результата оплаты в Kafka.

## Минимальное API

```http
POST /orders
GET /orders/{orderId}
```

## Интеграции

```text
order-service -> billing-service: POST /accounts/{userId}/withdraw
order-service -> Kafka: publish OrderPaymentResult
```

## Статусы заказа

```text
PAID
PAYMENT_FAILED
```

## TODO

- Выбрать стек сервиса.
- Описать модели request/response.
- Реализовать создание заказа.
- Реализовать publish события в Kafka.
- Добавить Dockerfile.
- Добавить Kubernetes/Helm values.
