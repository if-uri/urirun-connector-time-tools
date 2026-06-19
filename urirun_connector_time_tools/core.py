from __future__ import annotations

from datetime import datetime
import json
from importlib import resources
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import urirun

ROUTE_NOW = "time://host/clock/query/now"
CONNECTOR_ID = "time-tools"


def _json_resource(name: str) -> dict[str, Any]:
    text = resources.files(__package__).joinpath(name).read_text(encoding="utf-8")
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError(f"{name} must contain a JSON object")
    return data


def connector_manifest() -> dict[str, Any]:
    return _json_resource("connector.manifest.json")


@urirun.command(ROUTE_NOW, meta={"label": "Read current time", "connector": CONNECTOR_ID})
def now_command(timezone: str = "UTC", output: str = "iso") -> list[str]:
    """Declare the URI binding once; the function signature becomes the schema."""
    return ["urirun-time-tools", "now", "--timezone", "{timezone}", "--output", "{output}"]


def urirun_bindings() -> dict[str, Any]:
    return urirun.connector_bindings(connector=CONNECTOR_ID)


def now(timezone: str = "UTC", output: str = "iso") -> dict[str, Any]:
    try:
        tz = ZoneInfo(timezone)
    except ZoneInfoNotFoundError:
        return {
            "ok": False,
            "connector": CONNECTOR_ID,
            "timezone": timezone,
            "error": f"unknown timezone: {timezone}",
        }

    current = datetime.now(tz)
    epoch = int(current.timestamp())
    iso_value = current.isoformat()
    if output == "epoch":
        value: str | int = epoch
    elif output == "date":
        value = current.date().isoformat()
    else:
        value = iso_value

    return {
        "ok": True,
        "connector": CONNECTOR_ID,
        "timezone": timezone,
        "output": output,
        "value": value,
        "iso": iso_value,
        "epochSeconds": epoch,
        "utcOffset": current.strftime("%z"),
    }
