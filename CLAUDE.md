# CLAUDE.md

## Project Overview

jrnl is a command-line journal application written in Python. It supports plain text and encrypted (AES) journals, multiple journal types, and various export formats. The main branch for development is `develop`; PRs should target `develop`.

## Development Setup

```bash
pipx install poetry
poetry install
poetry shell  # activate virtualenv
```

## Common Commands

```bash
# Run full lint + test suite
poetry run poe test

# Run tests only (no linting)
poetry run poe test-run

# Run a single test file
poetry run pytest tests/unit/test_config_file.py

# Run a single BDD scenario by name (all BDD tests are in test_features.py)
poetry run pytest tests/bdd/test_features.py -k "test_scenario_name"

# Run a single test by name
poetry run pytest -k "test_name" -x

# Linting only
poetry run poe lint

# Auto-format code
poetry run poe format

# Serve docs locally at localhost:8000
poetry run poe docs-run
```

Tests run in parallel by default (`-n=auto` via pytest-xdist). To disable for debugging: `poetry run pytest -n0 -x`.

## Architecture

### Control Flow

Entry point: `jrnl/main.py:run()` → `jrnl/controller.py:run()`

The controller has a two-phase command model:
1. **Preconfig commands** (no config needed): `--help`, `--version`, `--diagnostic`
2. **Postconfig commands** (need config): `--encrypt`, `--decrypt`, `--import`, `--list`
3. Then either **append mode** (writing entries) or **search mode** (querying/filtering)
4. Search results can have actions applied: `--edit`, `--delete`, `--change-time`

CLI argument parsing is in `jrnl/args.py` (argparse-based).

### Journal Types (`jrnl/journals/`)

- `Journal` — base class, single-file storage, supports encryption
- `FolderJournal` — entries stored as individual files in year/month/day structure
- `DayOneJournal` — reads macOS Day One `.doentry` plist files

Factory: `open_journal()` in `jrnl/journals/__init__.py` selects type from config.

### Encryption (`jrnl/encryption/`)

- `BaseEncryption` (abstract) → `NoEncryption`, `BasePasswordEncryption`
- `BasePasswordEncryption` → `Jrnlv1Encryption` (legacy), `Jrnlv2Encryption` (current)
- `determine_encryption_method()` factory maps config values to classes

### Plugins (`jrnl/plugins/`)

Exporters: Text, Markdown, JSON, YAML, XML, Fancy, Tags, Dates, Calendar Heatmap. One importer: JRNL (native format). Plugin lookup via `get_exporter(format)` / `get_importer(format)`.

### Git Integration (`jrnl/git.py`)

Auto-commit, auto-pull, and auto-push are configurable per journal. `git_auto_commit()` initializes repos, stages changes, and commits. `git_pull()` uses fetch + fast-forward.

### Config (`jrnl/config.py`)

YAML-based config with per-journal overrides. Journals can be a string (path) or dict (path + overrides). CLI args override config via `apply_overrides()`.

## Testing

- **BDD tests**: `tests/bdd/features/*.feature` files using pytest-bdd. Step implementations in `tests/lib/` (`given_steps.py`, `when_steps.py`, `then_steps.py`, `fixtures.py`).
- **Unit tests**: `tests/unit/test_*.py`
- OS-specific markers: `@skip_win`, `@skip_posix`, `@on_win`, `@on_posix`
- CI tests across Python 3.10–3.14 on Linux, macOS, and Windows

## Code Style

- Formatter: black (line length 88)
- Linter: ruff (target Python 3.10)
- Import sorting: ruff with isort rules, force single-line imports
- Build system: poetry-core
