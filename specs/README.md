# Tuicade specs — demo run order

Each spec is sized to be handed to its own VS Code Copilot / Claude Code
session, so the whole arcade is built in parallel.

## Run order

| # | Spec | Session style | Recommended model |
|---|------|---------------|-------------------|
| 1 | [`00_launcher.md`](00_launcher.md) | Solo, **must finish first** | Sonnet 4.6 |
| 2 | [`01_hangman.md`](01_hangman.md) | Hand-started, parallel | Sonnet 4.6 |
| 3 | [`02_tictactoe.md`](02_tictactoe.md) | Hand-started, parallel | Sonnet 4.6 |
| 4 | [`03_word_scramble.md`](03_word_scramble.md) | Hand-started, parallel | Sonnet 4.6 |
| 5 | [`10_batch_simple_games.md`](10_batch_simple_games.md) | One coordinator → 3 subagents | Opus 4.7 (coord.) + Sonnet 4.6 (subs) |

After spec 1 merges, specs 2–4 can start in any order and run concurrently.
Spec 5 can start at the same time as 2–4 if you want maximum parallelism —
they still don't collide, because each game owns its own file pair.

## Why this can't produce merge conflicts

Every game spec writes exactly two files:

- `src/tuicade/games/<slug>.py`
- `tests/test_<slug>.py`

No two specs share a file. The launcher (spec 00) deliberately auto-discovers
games via `pkgutil.iter_modules`, so adding a game never edits launcher code.

## Design choices that make parallel sessions safe

- All dependencies — including `rich==15.0.0` — are pinned in
  `pyproject.toml` and locked in `uv.lock`. `make install` runs
  `uv sync --locked`, so every parallel session gets the exact same
  versions. Specs must not add new dependencies.
- Locked the `Game` contract (slug, title, description, run) in spec 00 and
  referenced it verbatim from every game spec — eliminates ambiguity when
  parallel agents decide field names.
- Forced `rich`-based but *visually distinct* rendering per game (gallows
  art for Hangman, a bordered grid for Tic-Tac-Toe, scrambled letters for
  Word Scramble, a dice-results panel for Dice Roll), so each game is
  recognisable at a glance.
- Scoped every spec to exactly two files and an explicit "do not edit any
  other file" rule, so parallel sessions literally cannot conflict.
- The batch coordinator (spec 10) produces a single PR for all three
  subagents, not three separate PRs — the point of that pattern is one
  batched result.
- Recommended models per spec: Sonnet for mechanical / narrow-scope work,
  Opus for the coordinator in plan mode.
- Hangman word list uses plain lowercase ASCII (no hyphens); the
  hyphen-handling rule lives only in Word Scramble's spec — keeps each
  spec's edge cases local and prevents cross-spec confusion for
  subagents.
