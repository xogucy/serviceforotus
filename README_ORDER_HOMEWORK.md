# Order Service Homework

Заготовка для ДЗ: сервис заказов, биллинг, уведомления и брокер сообщений.

## Выбранный вариант

Для практической реализации выбран гибридный подход:

- HTTP для синхронных операций, где нужен немедленный результат;
- Kafka для асинхронной доставки уведомлений.

Схема:

```text
client
  -> user-service
  -> order-service

user-service -> billing-service
order-service -> billing-service
order-service -> Kafka -> notification-service
```

## Сервисы

- `user-service` - пользователи.
- `billing-service` - счета, пополнение, списание денег.
- `order-service` - создание заказов и публикация результата оплаты.
- `notification-service` - сохранение уведомлений из брокера и выдача списка сообщений.

## Основной сценарий

1. Создать пользователя.
2. При создании пользователя создать счет в billing-service.
3. Пополнить счет пользователя.
4. Создать заказ, на который хватает денег.
5. Проверить, что деньги списались.
6. Проверить, что уведомление об успехе сохранено.
7. Создать заказ, на который денег не хватает.
8. Проверить, что баланс не изменился.
9. Проверить, что уведомление об ошибке сохранено.

## Установка

Namespace:

```text
orders-homework
```

Через Helm:

```bash
kubectl create namespace orders-homework
helm install orders-app ./deploy/helm/orders-homework -n orders-homework
```

Ingress host:

```text
arch.homework
```

## Локальный запуск через Docker Compose

Для разработки подготовлен общий `docker-compose.yml`.

Поднять только инфраструктуру:

```bash
make local-infra-up
```

Это запустит:

- PostgreSQL на `localhost:5432`
- Kafka на `localhost:9092`

Локально используется один контейнер PostgreSQL, но отдельные базы для сервисов:

```text
users_db
billing_db
orders_db
notifications_db
```

Поднять инфраструктуру и приложения:

```bash
make local-apps-up
```

Порты приложений:

```text
user-service:          http://localhost:8001
billing-service:       http://localhost:8002
order-service:         http://localhost:8003
notification-service:  http://localhost:8004
```

Пока `billing-service`, `order-service` и `notification-service` являются заготовками, профиль приложений может падать до реализации `app = FastAPI()`.

Остановить локальный контур:

```bash
make local-down
```

Сбросить локальные данные PostgreSQL:

```bash
make local-reset
```

Посмотреть статус:

```bash
make local-ps
```

## Newman

Postman environment должен содержать:

```text
baseUrl = http://arch.homework
```

Планируемая команда запуска:

```bash
newman run postman/orders-homework.postman_collection.json \
  -e postman/orders-homework.postman_environment.json \
  --reporters cli
```

## Где что лежит

- `services/` - папки будущих микросервисов.
- `docs/architecture.md` - архитектурные варианты и sequence diagrams.
- `docs/api-idl.md` - HTTP API и события.
- `deploy/helm/orders-homework/` - будущий Helm chart.
- `postman/` - будущие Postman/Newman артефакты.
