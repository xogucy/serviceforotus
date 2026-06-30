# API and Events IDL

Черновик контрактов. Перед реализацией можно уточнить поля и форматы ошибок.

## user-service

### Create user

```http
POST /users
Content-Type: application/json
```

Request:

```json
{
  "email": "user@example.com",
  "name": "Ivan"
}
```

Response:

```json
{
  "userId": "uuid",
  "email": "user@example.com",
  "name": "Ivan"
}
```

### Get user

```http
GET /users/{userId}
```

## billing-service

### Create account

```http
POST /accounts
Content-Type: application/json
```

Request:

```json
{
  "userId": "uuid"
}
```

### Get account

```http
GET /accounts/{userId}
```

### Deposit

```http
POST /accounts/{userId}/deposit
Content-Type: application/json
```

Request:

```json
{
  "amount": 1000
}
```

### Withdraw

```http
POST /accounts/{userId}/withdraw
Content-Type: application/json
```

Request:

```json
{
  "amount": 500
}
```

Response:

```json
{
  "success": true,
  "balance": 500
}
```

## order-service

### Create order

```http
POST /orders
Content-Type: application/json
```

Request:

```json
{
  "userId": "uuid",
  "email": "user@example.com",
  "price": 500
}
```

Response:

```json
{
  "orderId": "uuid",
  "userId": "uuid",
  "price": 500,
  "status": "PAID"
}
```

## notification-service

### Get user notifications

```http
GET /notifications/{userId}
```

Response:

```json
{
  "items": [
    {
      "notificationId": "uuid",
      "userId": "uuid",
      "email": "user@example.com",
      "message": "Order paid successfully"
    }
  ]
}
```

## Kafka event

Topic:

```text
order.payment.result
```

Event:

```json
{
  "eventId": "uuid",
  "eventType": "OrderPaymentResult",
  "orderId": "uuid",
  "userId": "uuid",
  "email": "user@example.com",
  "price": 500,
  "paymentStatus": "SUCCESS",
  "message": "Order paid successfully"
}
```

Allowed `paymentStatus` values:

```text
SUCCESS
FAILED
```
