# ==========================================
# Examen MLOps : mlops-nginx-exam-2
# ==========================================

PROJECT_NAME=mlops-nginx-exam-2

.PHONY: help clean start-project stop-project test logs-nginx

help: ## Affiche ce message d'aide
	@echo "-----------------------------------------------------------------------"
	@echo "Usage: make [COMMANDE]"
	@echo "-----------------------------------------------------------------------"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

clean: ## Vidage complet de la mémoire et des conteneurs fantômes
	@echo "🧹 Suppression de TOUS les conteneurs et libération de la RAM..."
	@docker rm -f $$(docker ps -aq) 2>/dev/null || echo "Aucun conteneur à supprimer."
	@docker system prune -f --volumes
	@sudo sync && echo 3 | sudo tee /proc/sys/vm/drop_caches
	@echo "✨ Système prêt et vierge."

start-project: clean ## Nettoie, build et lance l'infrastructure (API v1 x3, v2, Nginx)
	@echo "🚀 Démarrage des services..."
	docker compose -p $(PROJECT_NAME) up -d --build
	@echo "⏳ Attente du démarrage complet (10s)..."
	@sleep 10
	@echo "📊 État actuel des services :"
	docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

test: start-project ## Relance TOUT (Clean + Start) puis exécute les tests
	@echo "🧪 Lancement des tests (SSL, Auth, A/B Testing, Rate Limit)..."
	bash tests/run_tests.sh
	@echo "✅ Fin des tests globaux."

stop-project: ## Arrêt simple des services du projet actuel
	@echo "👋 Arrêt des services..."
	docker compose -p $(PROJECT_NAME) down
	@echo "✅ Services arrêtés."

logs-nginx: ## Affiche les logs de Nginx
	@echo "📋 Lecture des logs de Nginx..."
	docker logs -f mlops-nginx-1


