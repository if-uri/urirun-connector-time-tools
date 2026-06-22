#!/usr/bin/env bash
# time-tools: install once, then run — auto-discovered, no registry path.
set -euo pipefail
urirun install urirun-connector-time-tools            # local dev: pip install -e .
urirun run 'time://host/clock/query/now' --payload '{}' --execute --allow 'time://*'
