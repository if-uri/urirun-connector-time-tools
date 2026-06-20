# Author: Tom Sapletta · https://tom.sapletta.com
# Part of the ifURI solution.

from __future__ import annotations

import argparse
import json
import sys

from .core import connector_manifest, now, urirun_bindings


def emit(payload: dict) -> None:
    print(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="urirun-time-tools")
    sub = parser.add_subparsers(dest="command", required=True)
    r = sub.add_parser("now", help="Emit current time as structured JSON")
    r.add_argument("--timezone", default="UTC")
    r.add_argument("--output", choices=["iso", "epoch", "date"], default="iso")
    sub.add_parser("manifest", help="Emit the connect.ifuri.com connector manifest")
    sub.add_parser("bindings", help="Emit urirun v2 bindings")

    args = parser.parse_args(argv)
    if args.command == "now":
        result = now(timezone=args.timezone, output=args.output)
        emit(result)
        return 0 if result.get("ok") else 2
    if args.command == "manifest":
        emit(connector_manifest()); return 0
    if args.command == "bindings":
        emit(urirun_bindings()); return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
