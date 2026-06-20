#!/usr/bin/env bash
# Author: Tom Sapletta · https://tom.sapletta.com
# Part of the ifURI solution.

set -euo pipefail

mkdir -p .docker-smoke

echo "==> direct connector CLI"
urirun-time-tools now --timezone UTC --output iso > .docker-smoke/cli-result.json

echo "==> build bindings and registry"
python3 - <<'PY' > .docker-smoke/bindings.json
import json
from urirun_connector_time_tools import urirun_bindings
print(json.dumps(urirun_bindings(), indent=2))
PY

urirun validate .docker-smoke/bindings.json
urirun compile .docker-smoke/bindings.json --out .docker-smoke/registry.json

echo "==> execute connector URI through urirun"
urirun run 'time://host/clock/query/now' .docker-smoke/registry.json \
  --payload '{"timezone":"UTC","output":"date"}' \
  --execute \
  --allow 'time://host/*' > .docker-smoke/urirun-result.json

echo "==> project registry to MCP tools and A2A card"
python3 -m urirun.v2_mcp tools .docker-smoke/registry.json > .docker-smoke/mcp-tools.json
python3 -m urirun.v2_mcp card .docker-smoke/registry.json \
  --name time-tools-docker \
  --url http://tester/ > .docker-smoke/a2a-card.json

python3 - <<'PY'
import json
from pathlib import Path

base = Path(".docker-smoke")
cli = json.loads((base / "cli-result.json").read_text())
run = json.loads((base / "urirun-result.json").read_text())
run_payload = json.loads(run["result"]["stdout"])
tools = json.loads((base / "mcp-tools.json").read_text())
card = json.loads((base / "a2a-card.json").read_text())

assert cli["ok"] is True, cli
assert run["ok"] is True, run
assert run_payload["timezone"] == "UTC", run
assert any(tool["name"] == "time_host_clock_query" for tool in tools["tools"]), tools
assert any("time://host/clock/query/now" in skill.get("examples", []) for skill in card["skills"]), card
print(json.dumps({
    "ok": True,
    "timezone": cli["timezone"],
    "mcpTools": len(tools["tools"]),
    "a2aSkills": len(card["skills"]),
}, indent=2))
PY
