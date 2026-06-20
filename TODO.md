# TODO

## Connector roadmap

- [x] Expose `urirun_bindings()` through the stable `urirun.bindings`
      entry-point group.
- [ ] Add this connector to IFURI-016 full host-node Docker matrix with
      deterministic `time://` routes used by a flow.
- [ ] Add hub install smoke coverage for `time-tools`.
- [ ] Add more deterministic formats for flow use, for example epoch seconds,
      date-only and RFC3339.
- [ ] Add a sample flow that combines `time://` with `log://` and
      `planfile://` task scheduling.
- [ ] Keep the manifest and README examples aligned with the current `urirun`
      connector helper API.
- [ ] Publish route schemas and deterministic-output examples on the connector
      detail page.

## Related resources

- Hub page: https://connect.ifuri.com/connectors/time-tools
- Runtime: https://github.com/if-uri/urirun
- Examples: https://github.com/if-uri/examples
- Work summary: https://github.com/if-uri/docs/blob/main/work-summary-2026-06-20.md
