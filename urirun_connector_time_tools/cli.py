# Author: Tom Sapletta · https://tom.sapletta.com
# Part of the ifURI solution.

from __future__ import annotations

import sys

import urirun

from .core import connector_manifest, now, urirun_bindings


def register(sub) -> None:
    now_parser = sub.add_parser("now", help="Emit current time as structured JSON")
    now_parser.add_argument("--timezone", default="UTC")
    now_parser.add_argument("--output", choices=["iso", "epoch", "date"], default="iso")


def dispatch(args) -> int:
    if args.command == "now":
        result = now(timezone=args.timezone, output=args.output)
        urirun.connector_emit(result)
        return 0 if result.get("ok") else 2
    return 1


def main(argv: list[str] | None = None) -> int:
    return urirun.connector_cli(
        "urirun-time-tools",
        manifest=connector_manifest,
        bindings=urirun_bindings,
        register=register,
        dispatch=dispatch,
        argv=argv,
    )


if __name__ == "__main__":
    sys.exit(main())
