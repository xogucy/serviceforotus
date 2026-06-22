# serviceforotus

Простейший RESTful CRUD-сервис пользователей на FastAPI, PostgreSQL и Kubernetes.

## API

Базовый URL для Kubernetes: `http://arch.homework`.

- `GET /health/` - совместимый healthcheck для Postman
- `GET /live` - liveness probe
- `GET /ready` - readiness probe с проверкой БД
- `POST /users` - создать пользователя
- `GET /users` - получить список пользователей
- `GET /users/{id}` - получить пользователя
- `PUT /users/{id}` - обновить пользователя
- `DELETE /users/{id}` - удалить пользователя

Тело создания пользователя:

```json
{
  "username": "ivan",
  "firstName": "Ivan",
  "lastName": "Petrov",
  "email": "ivan@example.com",
  "phone": "+79990000000"
}
```

## Локальный запуск

```bash
cp .env.example .env
docker compose up --build db migrate app
```

После запуска сервис доступен на `http://localhost:8000`.

## Kubernetes

### Установка Ingress NGINX

```bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx/
helm repo update
helm upgrade --install nginx ingress-nginx/ingress-nginx -f chart/nginx-ingress.yaml
```

### Установка БД из Helm

```bash
helm upgrade --install users-db oci://registry-1.docker.io/bitnamicharts/postgresql -f helm/postgresql-values.yaml
```

Файл values для БД: `helm/postgresql-values.yaml`.

### Сборка образа приложения

```bash
docker build -t e1name/forotus:users-crud .
```

Если кластер не видит локальные Docker-образы, загрузите образ в Minikube:

```bash
minikube image load e1name/forotus:users-crud
```

Либо запушьте образ в registry и замените `image` в `chart/deployment.yaml` и `chart/migration-job.yaml`.

### Применение ConfigMap и Secret

```bash
kubectl apply -f chart/configmap.yaml
kubectl apply -f chart/secret.yaml
```

Конфигурация приложения лежит в `ConfigMap`, доступы к БД и `DATABASE_URL` - в `Secret`.

### Первоначальные миграции

```bash
kubectl apply -f chart/migration-job.yaml
kubectl wait --for=condition=complete job/users-service-migrations --timeout=120s
```

### Запуск приложения

```bash
kubectl apply -f chart/deployment.yaml
kubectl apply -f chart/service.yaml
kubectl apply -f chart/ingress.yaml
```

Та же команда одной строкой в правильном порядке:

```bash
kubectl apply -f chart/configmap.yaml -f chart/secret.yaml -f chart/migration-job.yaml -f chart/deployment.yaml -f chart/service.yaml -f chart/ingress.yaml
```

Для локального кластера добавьте запись в `/etc/hosts`, если ее еще нет:

```text
127.0.0.1 arch.homework
```

## Проверка Postman/Newman

Коллекция: `serviceforotus.postman_collection.json`. В ней используется базовый URL `http://arch.homework`.

```bash
newman run serviceforotus.postman_collection.json
```

Для локальной проверки через `docker compose`, без Ingress на `arch.homework`, можно запустить ту же коллекцию так:

```bash
newman run serviceforotus.postman_collection.json --env-var baseUrl=http://localhost:8000
```

Если Minikube/Ingress доступен через локальный port-forward, например:

```bash
kubectl port-forward -n m svc/nginx-ingress-nginx-controller 8080:80
newman run serviceforotus.postman_collection.json --env-var baseUrl=http://arch.homework:8080
```

Ожидаемый результат: все запросы `Healthcheck`, `Create user`, `Get user`, `Update user`, `Delete user` проходят без ошибок.
Пример успешного вывода сохранен в `newman-run.txt`.

## Директория с Kubernetes-манифестами

Манифесты находятся в директории `chart/`. Для сдачи задания укажите ссылку на эту директорию в pull request.
