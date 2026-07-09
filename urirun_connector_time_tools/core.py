# Author: Tom Sapletta · https://tom.sapletta.com
# Part of the ifURI solution.

"""Current-time route for urirun.

One typed ``@handler`` declares the route, its input schema (from the signature)
and its implementation — no argv template, no ``_exec.py``, no ``run_route``
dispatcher, no ``cli.py``. ``isolated=True`` runs the route out-of-process through
the shared ``python -m urirun.exec`` runner, so the binding stays
**registry-portable**: it executes from a compiled/served registry
(``urirun run``/``urirun node serve``, examples 12/19) with only the package
importable — no console-script install and no per-connector shim.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import urirun

from . import _urirun_compat

CONNECTOR_ID = "time-tools"
conn = _urirun_compat.connector(CONNECTOR_ID, scheme="time")


@conn.handler("clock/query/now", isolated=True, meta={"label": "Read current time"})
def now(timezone: str = "UTC", output: str = "iso") -> dict[str, Any]:
    """Return the current time in a timezone as iso / epoch / date."""
    try:
        tz = ZoneInfo(timezone)
    except ZoneInfoNotFoundError:
        return urirun.fail(f"unknown timezone: {timezone}", timezone=timezone)

    current = datetime.now(tz)
    epoch = int(current.timestamp())
    iso_value = current.isoformat()
    if output == "epoch":
        value: str | int = epoch
    elif output == "date":
        value = current.date().isoformat()
    else:
        value = iso_value

    return urirun.ok(
        timezone=timezone,
        output=output,
        value=value,
        iso=iso_value,
        epochSeconds=epoch,
        utcOffset=current.strftime("%z"),
    )


def urirun_bindings() -> dict[str, Any]:
    """Serializable v2 bindings for this connector (entry point: urirun.bindings)."""
    return conn.bindings()

@conn.handler("time://host/doctor/query/report", isolated=True, meta={"label": "Connector readiness report"})
def doctor() -> dict[str, Any]:
    """Return a safe, read-only connector readiness report for CI smoke tests."""
    return {
        "ok": True,
        "connector": CONNECTOR_ID,
        "version": _connector_version(),
        "status": "ready",
    }


def _connector_version() -> str:
    try:
        from importlib.metadata import version

        return version("urirun-connector-time-tools")
    except Exception:
        return "0.1.0"


def connector_manifest() -> dict[str, Any]:
    """Full manifest: prose (connector.manifest.json) + routes/uriSchemes/
    adapterKinds/examples derived from the handler."""
    return conn.manifest(_urirun_compat.load_manifest(__package__))


def main(argv: list[str] | None = None) -> int:
    """Console-script entry point: subcommands + dispatch derived from the handler."""
    return conn.cli(argv, manifest_prose=_urirun_compat.load_manifest(__package__))


if __name__ == "__main__":
    import sys

    raise SystemExit(main())
