# Spec 00 — Launcher and game plugin registry

**Run this spec first, alone.** Every other spec depends on the contract and
files this one creates. Do not start the game specs in parallel until this
session has finished and `make` is green.

**Recommended model:** Claude Sonnet 4.6. The work is mechanical scaffolding —
no deep planning needed. Agent mode; plan mode off.

## Goal

Turn `tuicade` from an empty `main()` into a working terminal arcade shell
with:

- A `rich`-based interactive menu (`uv run tuicade`).
- A plugin registry that auto-discovers games from `src/tuicade/games/`.
- A stable shared contract (`Game` dataclass + `GAME` module attribute) that
  every game spec references.

When this session completes, running `uv run tuicade` should show an empty
menu with a friendly "No games installed yet." message and a quit option.

## Files you will create or edit

Create:
- `src/tuicade/games/__init__.py` — empty package marker.
- `src/tuicade/launcher.py` — dataclass, discovery, menu loop.
- `tests/test_launcher.py` — discovery tests.

Edit:
- `pyproject.toml` — move `rich` from the `dev` dependency-group into
  `[project].dependencies`, keeping the exact pin: `rich==15.0.0`. After
  editing, re-run `uv lock` so `uv.lock` picks up the dependency-group
  change, and commit the updated `uv.lock` alongside `pyproject.toml`.
- `src/tuicade/tuicade.py` — replace the empty `main()` with a thin wrapper
  that calls the launcher.
- `src/tuicade/__init__.py` — export `main` and `Game` for public use.

**Do not** create any files under `src/tuicade/games/` other than
`__init__.py`. Individual games are owned by the other specs and will be
added by parallel sessions.

## Shared contract (this is the contract every game spec relies on — keep it stable)

```python
# src/tuicade/launcher.py
from dataclasses import dataclass
from typing import Callable

@dataclass(frozen=True)
class Game:
    slug: str              # stable id, e.g. "hangman"; also the module name
    title: str             # shown in the menu, e.g. "Hangman"
    description: str       # one-line menu help (<= 60 chars)
    run: Callable[[], None]  # blocking; returns when the player quits/finishes
```

Every game module at `src/tuicade/games/<slug>.py` must expose a module-level
constant named `GAME` of type `Game`. The launcher does not know anything
about individual games — it just iterates the package.

## Required functions in `launcher.py`

- `discover_games() -> list[Game]`
  - Iterate `pkgutil.iter_modules(tuicade.games.__path__, prefix="tuicade.games.")`.
  - Import each, read the `GAME` attribute. Skip modules that don't have one
    (log a `rich` warning; don't crash).
  - Return the list sorted by `title` (case-insensitive).

- `run_menu(console: rich.console.Console | None = None) -> None`
  - Loop until the user quits.
  - Render a `rich.table.Table` with columns: `#`, `Game`, `What it is`.
  - Footer line: `q` to quit.
  - Use `rich.prompt.Prompt.ask` to read the selection.
  - On valid numeric input, call `game.run()`; catch `KeyboardInterrupt` so
    Ctrl-C returns to the menu rather than killing the process.
  - After the game returns, clear the screen and redraw the menu.
  - If `discover_games()` returns `[]`, print
    `"No games installed yet. Drop a module into src/tuicade/games/."` and
    still accept `q`.

## Entry-point wiring

`src/tuicade/tuicade.py`:

```python
from tuicade.launcher import run_menu

def main() -> None:
    run_menu()

if __name__ == "__main__":
    main()
```

`pyproject.toml` `[project.scripts]` already points `tuicade` at
`tuicade:main`. Leave it as-is; just make sure `main` is re-exported from
`src/tuicade/__init__.py`.

## Tests (`tests/test_launcher.py`)

- `test_discover_games_empty` — with no game modules installed besides the
  package's own `__init__.py`, `discover_games()` returns `[]`.
- `test_discover_games_finds_stub` — create a stub module on disk inside
  `src/tuicade/games/` *using a pytest fixture that tears it down afterwards*,
  or use `monkeypatch` + `importlib` to inject a fake module whose `GAME`
  attribute is a known `Game`. Assert the launcher picks it up.
- `test_discover_games_skips_module_without_game` — inject a module that
  lacks `GAME`; assert it's skipped without raising.

Do **not** test `run_menu` interactively — keep tests pure.

## Definition of done

- `uv sync` succeeds with `rich` as a runtime dep.
- `make` passes (ruff, basedpyright, codespell, pytest) from `tuicade/`.
- `uv run tuicade` opens the empty menu and quits cleanly on `q`.
- Commits are granular: one commit for deps, one for the registry, one for
  the menu, one for tests.
- Open a PR titled `feat: launcher and plugin registry` and list test counts
  in the description (per `CLAUDE.md` workflow).
