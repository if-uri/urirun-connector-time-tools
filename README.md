# urirun-connector-time-tools

Time Tools connector for [ifURI](https://ifuri.com) / [urirun](https://github.com/if-uri/urirun).

Public hub page:
[connect.ifuri.com/connectors/time-tools](https://connect.ifuri.com/connectors/time-tools)

- Declares `time://` URI routes with `@conn.handler(..., isolated=True)` — the typed
  function body is the implementation, run out-of-process from a compiled registry.
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

After installation, `urirun` can discover this connector automatically through
the `urirun.bindings` entry-point group:

```bash
urirun discover --out connectors.bindings.json --registry-out connectors.registry.json
urirun list --entry-points
```

The route is declared once. The connector id and URI scheme are initialized once,
then each route is a single typed `@conn.handler`; `isolated=True` makes urirun run
it out-of-process (registry-portable) via the shared `python -m urirun.exec` runner:

```python
import urirun

conn = urirun.connector("time-tools", scheme="time")

@conn.handler("clock/query/now", isolated=True, meta={"label": "Read current time"})
def now(timezone: str = "UTC", output: str = "iso") -> dict:
    # the function body IS the implementation; it returns a structured result
    return urirun.ok(now="2026-01-01T00:00:00Z", timezone=timezone)
```

`conn.bindings()` turns that declaration into the registry input used by
CLI, host flows, MCP tools and A2A skills.

## Related projects

- Runtime: [if-uri/urirun](https://github.com/if-uri/urirun)
- Docs: [docs.ifuri.com/connectors.html](https://docs.ifuri.com/connectors.html) · [authoring a connector](https://docs.ifuri.com/connector-authoring.html)
- Hub page: [connect.ifuri.com/connectors/time-tools](https://connect.ifuri.com/connectors/time-tools)
- Connector hub: [connect.ifuri.com](https://connect.ifuri.com)
- Examples: [if-uri/examples](https://github.com/if-uri/examples)
- Current work summary:
  [work-summary-2026-06-20](https://github.com/if-uri/docs/blob/main/work-summary-2026-06-20.md)

Repository notes: [TODO.md](TODO.md) · [CHANGELOG.md](CHANGELOG.md)

## License

Released under the terms in [LICENSE](LICENSE).
