# Architecture

В этом файле описываются варианты взаимодействия сервисов для теоретической части ДЗ.

## Вариант 1. Только HTTP

Все сервисы взаимодействуют синхронно по HTTP.

```mermaid
sequenceDiagram
    actor Client
    participant User as user-service
    participant Billing as billing-service
    participant Order as order-service
    participant Notify as notification-service

    Client->>User: POST /users
    User->>Billing: POST /accounts
    Billing-->>User: account created
    User-->>Client: user created

    Client->>Order: POST /orders
    Order->>Billing: POST /accounts/{userId}/withdraw
    Billing-->>Order: payment result
    Order->>Notify: POST /notifications
    Notify-->>Order: notification saved
    Order-->>Client: order result
```

## Вариант 2. HTTP + broker for notifications

Платеж выполняется синхронно по HTTP, уведомление доставляется асинхронно через брокер.

```mermaid
sequenceDiagram
    actor Client
    participant Order as order-service
    participant Billing as billing-service
    participant Broker as Kafka
    participant Notify as notification-service

    Client->>Order: POST /orders
    Order->>Billing: POST /accounts/{userId}/withdraw
    Billing-->>Order: payment result
    Order->>Broker: publish OrderPaymentResult
    Broker-->>Notify: consume OrderPaymentResult
    Notify->>Notify: save notification
    Order-->>Client: order result
```

Этот вариант выбран для практической реализации.

## Вариант 3. Event Collaboration

Сервисы реагируют на события друг друга. Центрального синхронного процесса меньше, больше асинхронного обмена.

```mermaid
sequenceDiagram
    actor Client
    participant Order as order-service
    participant Broker as Kafka
    participant Billing as billing-service
    participant Notify as notification-service

    Client->>Order: POST /orders
    Order->>Broker: publish OrderCreated
    Broker-->>Billing: consume OrderCreated
    Billing->>Billing: withdraw money
    Billing->>Broker: publish PaymentSucceeded or PaymentFailed
    Broker-->>Order: consume payment result
    Order->>Order: update order status
    Broker-->>Notify: consume payment result
    Notify->>Notify: save notification
    Order-->>Client: order accepted
```

## Вариант 4. Итоговый выбор

Для реализации выбран вариант 2:

```text
HTTP + Kafka for notifications
```

Причины:

- результат оплаты нужен order-service сразу;
- уведомление можно выполнять асинхронно;
- схема проще полноценного Event Collaboration;
- архитектура потом расширяется до Saga Orchestration.
