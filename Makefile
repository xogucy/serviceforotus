PYTHON := .venv/bin/python

.PHONY: install run test deploy delete

install:
	$(PYTHON) -m pip install -r requirements.txt
	npm install -g newman

run:
	$(PYTHON) -m uvicorn main:app --host 0.0.0.0 --port 8000

test:
	newman run serviceforotus.postman_collection.json

deploy:
	kubectl create namespace m --dry-run=client -o yaml | kubectl apply -f -
	helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx/
	helm repo update
	helm upgrade --install nginx ingress-nginx/ingress-nginx -n m -f chart/nginx-ingress.yaml
	kubectl rollout status daemonset/nginx-ingress-nginx-controller -n m --timeout=180s
	sleep 10
	kubectl apply -f chart/deployment.yaml
	kubectl apply -f chart/service.yaml
	sleep 5
	kubectl apply -f chart/ingress.yaml

delete:
	kubectl delete -f chart/ingress.yaml --ignore-not-found=true
	kubectl delete -f chart/service.yaml --ignore-not-found=true
	kubectl delete -f chart/deployment.yaml --ignore-not-found=true
	helm uninstall nginx -n m || true
	kubectl delete namespace m --ignore-not-found=true --wait=false
