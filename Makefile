# Nom du projet pour Docker Compose
PROJECT_NAME=mlops

check-stop:
	@if [ "$$(docker compose -p $(PROJECT_NAME) ps -q)" != "" ]; then \
		echo "Arrêt des conteneurs existants..."; \
		docker compose -p $(PROJECT_NAME) down; \
	else \
		echo "Aucun conteneur actif"; \
	fi

start-project: check-stop
	docker compose -p $(PROJECT_NAME) up -d --build
	@echo "Services démarrés ✅"
	docker ps -a
	@echo "Vérification des services démarrés ✅"

stop-project:
	docker compose -p $(PROJECT_NAME) down
	@echo "Services arrêtés ✅"
	docker ps -a
	@echo "Vérification des services arrêtés ✅"

test: start-project
	@echo "⏳ Attente du démarrage complet des services (10s)..."
	@sleep 10
	@echo "🚀 Lancement des tests globaux (SSL, Auth, A/B, Rate Limit)..."
	python3 tests/tests_global.py

logs-nginx:
	docker logs -f mlops-nginx-1
