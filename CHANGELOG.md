# Changelog

## [Unreleased]

### Added
- Add connector TODO for hub install smoke, extra time formats and flow
  examples.
- Link README to the public connector hub page, examples and current
  cross-repository work summary.

## [0.1.2] - 2026-06-20

### Changed
- Require `urirun` `v0.3.14` so connector installs use the runtime with stable
  unique MCP/A2A tool names.

## [0.1.1] - 2026-06-20

### Changed
- Use `urirun.connector(...)` in connector code and docs so connector id,
  default URI target and binding export are declared once.
- Require `urirun` `v0.3.13`, where the connector helper is available.

## [0.1.0] - 2026-06-20

### Added
- Add the initial `time://host/clock/query/now` connector package with CLI,
  registry binding export, Docker smoke test, MCP projection and A2A projection.
