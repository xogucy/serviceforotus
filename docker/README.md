# Local Docker Compose

Локальный контур для разработки ДЗ с заказами.

## Команды

Поднять только инфраструктуру:

```bash
make local-infra-up
```

Поднять инфраструктуру и приложения:

```bash
make local-apps-up
```

Остановить:

```bash
make local-down
```

Сбросить данные PostgreSQL:

```bash
make local-reset
```

Посмотреть контейнеры:

```bash
make local-ps
```

Логи:

```bash
make local-logs
```

Логи конкретного сервиса:

```bash
./scripts/local-logs.sh postgres
```

## Порты

```text
PostgreSQL:            localhost:5432
Kafka:                 localhost:9092
user-service:          http://localhost:8001
billing-service:       http://localhost:8002
order-service:         http://localhost:8003
notification-service:  http://localhost:8004
```

## Базы данных

В локальном окружении используется один PostgreSQL контейнер и отдельная база на сервис:

```text
users_db
billing_db
orders_db
notifications_db
```

Инициализация баз описана в `docker/postgres/init/01-create-databases.sql`.

## Kafka

Локально используется Kafka в KRaft-режиме, без Zookeeper.

Topic для уведомлений:

```text
order.payment.result
```

Topic создается сервисом `kafka-init` при запуске инфраструктуры.
