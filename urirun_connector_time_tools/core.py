# Author: Tom Sapletta · https://tom.sapletta.com
# Part of the ifURI solution.

from __future__ import annotations

from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import urirun

ROUTE_NOW = "time://host/clock/query/now"
CONNECTOR_ID = "time-tools"
CONNECTOR = urirun.connector(CONNECTOR_ID, scheme="time")


def connector_manifest() -> dict[str, Any]:
    return urirun.load_manifest(__package__)


@CONNECTOR.command("clock/query/now", meta={"label": "Read current time"})
def now_command(timezone: str = "UTC", output: str = "iso") -> list[str]:
    """Declare the URI binding once; the function signature becomes the schema."""
    return ["urirun-time-tools", "now", "--timezone", "{timezone}", "--output", "{output}"]


def urirun_bindings() -> dict[str, Any]:
    return CONNECTOR.bindings()


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
