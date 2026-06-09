# AGENTS.md

## Project Overview

**act-template-python** is a [Copier](https://copier.readthedocs.io/) template for scaffolding new ACT (Agent Component Tools) components in Python.

Generated projects include: componentize-py build, WIT bindings, justfile, e2e tests (pytest + fastmcp, driving the component over MCP), CI (GitHub Actions), pre-commit hooks (prek), and licenses. Existing components can pull template updates via `copier update`.

## Scaffold a new component

```bash
copier copy gh:actcore/act-template-python my-component
cd my-component
just init    # fetch WIT deps
just build   # build wasm component
just test    # run e2e tests
```

## Repository Structure

```
copier.yml              # Copier config (questions, _subdirectory, _skip_if_exists)
AGENTS.md               # This file (not copied to projects)
CHANGELOG.md            # Template version history (not copied)
template/               # _subdirectory — only this gets copied to new projects
  pyproject.toml        # Python project config ({{ project_name }} placeholder)
  app.py                # Component source with ToolProvider class
  act.toml              # Component metadata + capabilities
  wit/
    world.wit           # WIT world definition (exports act:core/tool-provider@0.2.0)
    deps.toml           # wit-deps manifest (fetches act-core from act-spec)
  e2e/
    conftest.py         # Fixtures: act_command, wasm_path, connected MCP client
    pyproject.toml      # Suite's own dependency set (uv virtual project)
    test_info.py        # Smoke test: packed manifest reports name + version
    test_tools.py       # Smoke test: the component lists at least one tool
  justfile              # Recipes: init, setup, build, test, publish
  skill/SKILL.md        # Embedded agent skill
  prek.toml             # Pre-commit hooks: ruff check, ruff format
  .github/workflows/ci.yml  # CI: build, e2e, lint, publish
  .github/dependabot.yml    # Dependabot for pip + github-actions
  .gitignore            # *.wasm, __pycache__, wit/deps/, .venv/
  .python-version       # Python version pin (3.14)
  README.md
  LICENSE-MIT
  LICENSE-APACHE
```

## Template Variables

| Variable | Prompt | Used in |
|----------|--------|---------|
| `project_name` | "Component name (e.g. my-tool)" | pyproject.toml, justfile, e2e/conftest.py, e2e/test_info.py, skill/SKILL.md |
| `description` | "Component description" | pyproject.toml, README.md, skill/SKILL.md |
| `needs_filesystem` | "Does this component need filesystem access?" | act.toml |

## Jinja2 / Runtime Variable Conflicts

Files with runtime `{{ }}` variables (justfile) use `{% raw %}` blocks to prevent Jinja2 from interpreting them. Only Copier placeholders are outside raw blocks.

## Development Patterns

- **WIT deps**: managed by `wit-deps` (not git submodules). Run `just init` to fetch.
- **Build**: `componentize-py` compiles Python to WASM component, `wasm-tools` adds metadata, `cbor2` encodes custom section.
- **Package manager**: `uv` for dependencies and virtualenv.
- **Testing**: pytest + fastmcp driving `act run --mcp` over stdio, so tests observe what an agent observes.
- **CI**: `astral-sh/setup-uv` + `moonrepo/setup-rust` for toolchain + bins.
- **Pre-commit**: `prek` (ruff check, ruff format, yaml/toml checks).
- **Template sync**: `copier update` pulls template changes into existing components.

## Commands (in generated projects)

```bash
just init    # wit-deps: fetch WIT dependencies
just setup   # init + prek install (dev environment)
just build   # componentize-py + wasm-tools metadata + cbor custom section
just test    # pytest e2e suite over MCP (does NOT build, run just build first)
just publish # oras push to OCI registry
```

## Conventions

- Conventional commits
- Always include "act" in keywords
- `uv` over pip/pipenv
- `.python-version` pins Python 3.14
- `ruff` for linting and formatting
