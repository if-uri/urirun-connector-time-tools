.PHONY: help manifest bindings smoke test
help: ## List targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "}{printf "  %-10s %s\n",$$1,$$2}'
manifest: ## Print the connector manifest
	urirun-time-tools manifest
bindings: ## Print urirun bindings
	urirun-time-tools bindings
smoke: ## bindings -> urirun connectors smoke (validate/compile/run/MCP/A2A)
	urirun-time-tools bindings | urirun connectors smoke - \
	  --run 'time://host/clock/query/now' --payload '{"timezone":"UTC","output":"iso"}' \
	  --allow 'time://host/*' --name time-tools
test: ## Install editable + smoke
	pip install -e . && python3 -m pytest -q && $(MAKE) smoke

.PHONY: docker-test
docker-test: ## Run connector in Docker and verify registry, MCP and A2A
	docker compose up --build --abort-on-container-exit --exit-code-from tester
	docker compose down -v --remove-orphans
