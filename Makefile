.PHONY: help manifest bindings smoke test
help: ## List targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "}{printf "  %-10s %s\n",$$1,$$2}'
manifest: ## Print the connector manifest
	urirun-time-tools manifest
bindings: ## Print urirun bindings
	urirun-time-tools bindings
smoke: ## bindings -> urirun validate/compile/run -> MCP tools
	urirun-time-tools bindings > /tmp/time-tools.bindings.json
	urirun validate /tmp/time-tools.bindings.json
	urirun compile /tmp/time-tools.bindings.json --out /tmp/time-tools.registry.json
	urirun run 'time://host/clock/query/now' /tmp/time-tools.registry.json \
	  --payload '{"timezone":"UTC","output":"iso"}' --execute --allow 'time://host/*'
	python3 -m urirun.v2_mcp tools /tmp/time-tools.registry.json
	python3 -m urirun.v2_mcp card /tmp/time-tools.registry.json --name time-tools --url http://localhost/
test: ## Install editable + smoke
	pip install -e . && python3 -m pytest -q && $(MAKE) smoke

.PHONY: docker-test
docker-test: ## Run connector in Docker and verify registry, MCP and A2A
	docker compose up --build --abort-on-container-exit --exit-code-from tester
	docker compose down -v --remove-orphans
