# Changelog

All notable changes to this template are documented here.

Downstream components generated from this template should note which version they were created from and apply relevant entries when upgrading.

## [0.1.0] - 2026-04-01

### Added
- Initial Python component template with componentize-py, uv, cbor2
- `app.py` with hello tool (ToolProvider class)
- `act.toml` manifest with optional `wasi:filesystem` capability
- WIT world exporting `act:core/tool-provider@0.2.0`
- justfile with init, setup, build, test, publish recipes
- `skill/SKILL.md` embedded agent skill
- hurl e2e smoke tests (info + tools endpoints)
- GitHub Actions CI (build, e2e, lint, publish)
- prek pre-commit hooks (ruff check, ruff format, yaml, toml)
- dependabot config for pip + github-actions
- MIT + Apache-2.0 dual license
