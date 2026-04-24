# tuicade

A tiny arcade in the terminal — a launcher plus six small games (Hangman,
Tic-Tac-Toe, Word Scramble, Number Guessing, Dice Roll, Rock-Paper-Scissors).

> **This is an example project.** Its real purpose is to demonstrate how to
> build a small but complete application using **parallel agent sessions** in
> VS Code — multiple Copilot / Claude Code sessions working on the same repo
> at the same time without stepping on each other, plus one Claude Code
> coordinator session that fans out to subagents.

## Run it

```bash
uv run tuicade
```

Pick a game from the menu. Press `q` inside any game to return to the launcher.

## How it was built

Every game is a self-contained module under `src/tuicade/games/`, and the
launcher auto-discovers them with `pkgutil.iter_modules`. That's the whole
trick: adding a game never edits the launcher, so N sessions can write N
games in parallel with zero merge conflicts.

The recipe — spec order, recommended model per spec — lives in
[`specs/README.md`](specs/README.md). Clone the repo, open the specs in the
order listed, and you can reproduce the whole build.

## Development

- `make` — install, lint, and test (default target)
- `make build` — build sdist and wheel
- `make clean` — remove build artifacts and caches
- `uv run pytest` — run tests only
- `uv run python devtools/lint.py` — run linting only (ruff, basedpyright, codespell)

For how to install uv and Python, see [installation.md](docs/installation.md).
For development workflows, see [development.md](docs/development.md).
For instructions on publishing to PyPI, see [publishing.md](docs/publishing.md).

---

*This project was built from
[simple-modern-uv](https://github.com/jlevy/simple-modern-uv).*
