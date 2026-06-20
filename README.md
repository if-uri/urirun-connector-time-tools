# urirun-connector-time-tools

Time Tools connector for [ifURI](https://ifuri.com) / [urirun](https://github.com/tellmesh/urirun).

Public hub page:
[connect.ifuri.com/connectors/time-tools](https://connect.ifuri.com/connectors/time-tools)

- Declares `time://` URI routes with `@connector.command(...)`.
- `connector.manifest.json` is the connect.ifuri.com catalog entry (validated by schema).
- CLI: `urirun-time-tools now` · `urirun-time-tools manifest` · `urirun-time-tools bindings`.

## URI routes

| URI | Purpose |
| --- | --- |
| `time://host/clock/query/now` | Return current time for a timezone as JSON. |

## Quick start
```bash
pip install -e .
urirun-time-tools now --timezone UTC --output iso
make smoke        # bindings -> urirun validate/compile/run -> MCP tools + A2A card
```

The route is declared once. The connector id and URI scheme are initialized once,
then each route can use a short path:

```python
import urirun

connector = urirun.connector("time-tools", scheme="time")

@connector.command("clock/query/now")
def now_command(timezone: str = "UTC", output: str = "iso") -> list[str]:
    return ["urirun-time-tools", "now", "--timezone", "{timezone}", "--output", "{output}"]
```

`connector.bindings()` turns that declaration into the registry input used by
CLI, host flows, MCP tools and A2A skills.

## Related projects

- Runtime: [tellmesh/urirun](https://github.com/tellmesh/urirun)
- Connector hub: [connect.ifuri.com](https://connect.ifuri.com)
- Examples: [if-uri/examples](https://github.com/if-uri/examples)
- Current work summary:
  [work-summary-2026-06-20](https://github.com/if-uri/docs/blob/main/work-summary-2026-06-20.md)

Repository notes: [TODO.md](TODO.md) · [CHANGELOG.md](CHANGELOG.md)
