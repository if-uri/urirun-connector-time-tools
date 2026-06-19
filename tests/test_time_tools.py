from __future__ import annotations

import json

from urirun import v2
from urirun_connector_time_tools import connector_manifest, now, urirun_bindings
from urirun_connector_time_tools.cli import main


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


def test_manifest_shape() -> None:
    manifest = connector_manifest()
    assert manifest["id"] == "time-tools"
    assert "time://host/clock/query/now" in manifest["routes"]


def test_bindings_shape() -> None:
    bindings = urirun_bindings()
    route = bindings["bindings"]["time://host/clock/query/now"]
    assert route["argv"] == [
        "urirun-time-tools",
        "now",
        "--timezone",
        "{timezone}",
        "--output",
        "{output}",
    ]
    assert route["inputSchema"]["properties"]["timezone"]["default"] == "UTC"
    assert route["inputSchema"]["properties"]["output"]["default"] == "iso"


def test_bindings_are_json_serializable_and_compile() -> None:
    bindings = urirun_bindings()
    json.dumps(bindings)
    registry = v2.compile_registry(bindings)
    routes = v2.list_routes(registry)
    assert any(route["uri"] == "time://host/clock/query/now" for route in routes)


def test_cli_now(capsys) -> None:
    assert main(["now", "--timezone", "UTC", "--output", "date"]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["ok"] is True
    assert output["output"] == "date"


def test_cli_bindings(capsys) -> None:
    assert main(["bindings"]) == 0
    output = json.loads(capsys.readouterr().out)
    assert "time://host/clock/query/now" in output["bindings"]
