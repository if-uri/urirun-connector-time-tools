# Author: Tom Sapletta · https://tom.sapletta.com
# Part of the ifURI solution.

from __future__ import annotations

import json

import urirun
from urirun import v2
from urirun_connector_time_tools import connector_manifest, main, now, urirun_bindings
from urirun_connector_time_tools.core import conn

ROUTE = "time://host/clock/query/now"


def test_now_returns_structured_time() -> None:
    result = now(timezone="UTC", output="iso")
    assert result["ok"] is True
    assert result["timezone"] == "UTC"
    assert result["iso"].endswith("+00:00")
    assert isinstance(result["epochSeconds"], int)


def test_now_rejects_unknown_timezone() -> None:
    result = now(timezone="Not/AZone")
    assert result["ok"] is False
    assert "unknown timezone" in result["error"]


def test_bindings_are_isolated_handler() -> None:
    b = urirun_bindings()["bindings"][ROUTE]
    # registry-portable in-process handler: runs out-of-process via urirun.exec
    assert b["adapter"] == "local-function-subprocess"
    assert b["python"]["module"] == "urirun_connector_time_tools.core"
    assert b["python"]["export"] == "now"
    assert "argv" not in b
    json.dumps(urirun_bindings())  # serializable: no live ref leaks


def test_runtime_executes_from_compiled_registry() -> None:
    # the whole point: a serialized->compiled registry still runs the route
    registry = urirun.compile_registry(json.loads(json.dumps(urirun_bindings())))
    env = v2.run(ROUTE, registry, payload={"timezone": "UTC", "output": "date"},
                 mode="execute", policy=urirun.policy(allow=["time://*"]))
    assert env["ok"] is True
    data = urirun.result_data(env)
    assert data["ok"] is True and data["output"] == "date"


def test_manifest_prose_plus_derived() -> None:
    m = connector_manifest()
    assert m["id"] == "time-tools"
    assert m["routes"] == [ROUTE]
    assert m["uriSchemes"] == ["time"]
    assert m["summary"]  # prose preserved


def test_cli_bindings_and_manifest(capsys) -> None:
    assert main(["bindings"]) == 0
    assert ROUTE in json.loads(capsys.readouterr().out)["bindings"]
    assert main(["manifest"]) == 0
    assert json.loads(capsys.readouterr().out)["id"] == "time-tools"


def test_contract_output_shape() -> None:
    """Live output must satisfy the declared contract out-schema."""
    import importlib.util, sys
    sys.path.insert(0, "/home/tom/github/if-uri/urirun-contract")
    from urirun_connectors_toolkit.contract_gate import validate_output
    spec = importlib.util.spec_from_file_location(
        "contracts_time_tools",
        "/home/tom/github/if-uri/urirun-connector-time-tools/urirun_connector_time_tools/contracts.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    result = now(timezone="UTC", output="iso")
    assert result["ok"] is True
    validate_output(mod.CONTRACTS["clock/query/now"], result)
