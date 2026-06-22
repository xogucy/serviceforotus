PYTHON ?= python3
IMAGE ?= e1name/forotus:users-crud

.PHONY: install run migrate test docker-build db-install deploy delete

install:
	$(PYTHON) -m pip install -r requirements.txt
	npm install -g newman

run:
	$(PYTHON) -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --app-dir src

migrate:
	alembic upgrade head

test:
	newman run serviceforotus.postman_collection.json

docker-build:
	docker build -t $(IMAGE) .

db-install:
	helm upgrade --install users-db oci://registry-1.docker.io/bitnamicharts/postgresql -f helm/postgresql-values.yaml

deploy:
	helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx/
	helm repo update
	helm upgrade --install nginx ingress-nginx/ingress-nginx -f chart/nginx-ingress.yaml
	kubectl apply -f chart/configmap.yaml
	kubectl apply -f chart/secret.yaml
	kubectl apply -f chart/migration-job.yaml
	kubectl wait --for=condition=complete job/users-service-migrations --timeout=120s
	kubectl apply -f chart/deployment.yaml
	kubectl apply -f chart/service.yaml
	kubectl apply -f chart/ingress.yaml

delete:
	kubectl delete -f chart/ingress.yaml --ignore-not-found=true
	kubectl delete -f chart/service.yaml --ignore-not-found=true
	kubectl delete -f chart/deployment.yaml --ignore-not-found=true
	kubectl delete -f chart/migration-job.yaml --ignore-not-found=true
	kubectl delete -f chart/secret.yaml --ignore-not-found=true
	kubectl delete -f chart/configmap.yaml --ignore-not-found=true
	helm uninstall nginx || true
