# Author: Tom Sapletta · https://tom.sapletta.com
# Part of the ifURI solution.
"""Route contracts for the time-tools connector — clock query, read-only."""
from __future__ import annotations

from urirun_connectors_toolkit.contract_gate import Contract

CONTRACTS: dict[str, Contract] = {
    "clock/query/now": Contract(
        version="v1",
        effect="query",
        reversible=False,
        inp={"timezone": "?str", "output": "?str"},
        out={"oneOf": [
            {"ok": "const:true", "iso": "str", "epochSeconds": "int",
             "utcOffset": "str", "timezone": "str", "output": "str", "value": "any"},
            {"ok": "const:false", "error": "str", "timezone": "?str"},
        ]},
        errors=("precondition-unmet",),
        examples=(
            {
                "payload": {"timezone": "UTC"},
                "result": {
                    "ok": True,
                    "connector": "time-tools",
                    "iso": "2026-06-29T12:00:00+00:00",
                    "epochSeconds": 1751198400,
                    "utcOffset": "+0000",
                    "timezone": "UTC",
                    "output": "iso",
                    "value": "2026-06-29T12:00:00+00:00",
                },
            },
        ),
    ),
}
