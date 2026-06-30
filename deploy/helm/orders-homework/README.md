# orders-homework Helm chart

Здесь будет Helm chart для установки всех компонентов ДЗ.

Планируемые компоненты:

- user-service
- billing-service
- order-service
- notification-service
- Kafka
- Ingress для `arch.homework`

Команда установки:

```bash
kubectl create namespace orders-homework
helm install orders-app ./deploy/helm/orders-homework -n orders-homework
```
