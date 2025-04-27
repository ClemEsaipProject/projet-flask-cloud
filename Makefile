.PHONY: test build push deploy all clean

# Variables
APP_NAME = flask-static-app
REGISTRY = localhost:32000
TAG = latest

# Commandes
test:
	@echo "Exécution des tests unitaires..."
	pytest -v tests/

build: test
	@echo "Construction de l'image Docker..."
	docker build -t $(APP_NAME):$(TAG) .
	docker tag $(APP_NAME):$(TAG) $(REGISTRY)/$(APP_NAME):$(TAG)

push: build
	@echo "Publication de l'image sur le registre local..."
	docker push $(REGISTRY)/$(APP_NAME):$(TAG)

deploy: push
	@echo "Déploiement sur MicroK8s..."
	kubectl apply -f kubernetes/configmap.yaml
	kubectl apply -f kubernetes/deployment.yaml
	kubectl apply -f kubernetes/service.yaml
	kubectl rollout status deployment/flask-app

status:
	@echo "Vérification de l'état du déploiement..."
	kubectl get pods
	kubectl get services

logs:
	@echo "Affichage des logs..."
	kubectl logs -l app=flask-app --tail=100

all: deploy status

clean:
	@echo "Nettoyage des ressources..."
	kubectl delete -f kubernetes/
