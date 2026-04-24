# Spec 01 — Hangman

**Prerequisite:** Spec `00_launcher.md` has already been merged. The `Game`
dataclass, the `tuicade.games` package, and the launcher exist.

**Recommended model:** Claude Sonnet 4.6. Agent mode.

**Parallel-safe:** Yes. This spec only creates two files; no other spec
touches them.

## Goal

Add a Hangman game that plugs into the launcher via the shared `Game`
contract from `src/tuicade/launcher.py`.

## Files you will create

- `src/tuicade/games/hangman.py`
- `tests/test_hangman.py`

**Do not edit any other file.** If you find yourself wanting to change the
launcher or `pyproject.toml`, stop and ask — it means the contract from spec
00 needs adjustment, and that should happen in a separate session to avoid
merge conflicts with other parallel game sessions.

## Gameplay

- Word pool is a small built-in list (~20 AI/ML terms) hardcoded in the
  module. Examples: `transformer`, `embedding`, `gradient`, `tokenizer`,
  `attention`, `softmax`, `backprop`, `perceptron`, `dropout`, `activation`,
  `convolution`, `recurrence`, `sampler`, `logits`, `dataset`, `epoch`,
  `checkpoint`, `inference`, `prompt`, `context`. Feel free to adjust
  wording, but keep all lowercase ASCII letters (no hyphens, no spaces).
- 6 wrong guesses allowed. Draw an ASCII gallows that grows with each wrong
  guess; use `rich` for color (red for wrong, green for right).
- Show: current masked word, letters guessed so far (sorted), guesses left,
  the gallows.
- Input: one letter at a time. Repeat guesses are rejected with a gentle
  message and do not consume an attempt. `q` quits back to the launcher.
- On win: green "You saved them!" + the word. On loss: red
  "You lost — the word was: …". Pause for Enter, then return.

## Shape of the code

```python
# src/tuicade/games/hangman.py
from dataclasses import dataclass, field
from tuicade.launcher import Game

@dataclass
class HangmanState:
    word: str
    guessed: set[str] = field(default_factory=set)
    wrong: int = 0

def apply_guess(state: HangmanState, letter: str) -> HangmanState: ...
def is_won(state: HangmanState) -> bool: ...
def is_lost(state: HangmanState, max_wrong: int = 6) -> bool: ...
def render_word(state: HangmanState) -> str: ...

def play() -> None:
    ...  # interactive loop using rich.console.Console

GAME = Game(
    slug="hangman",
    title="Hangman",
    description="Guess the AI/ML word before the stickman falls.",
    run=play,
)
```

## Tests (`tests/test_hangman.py`)

Pure-logic only — do not test the interactive loop.

- `apply_guess` with a correct letter adds it to `guessed` and does not
  increment `wrong`.
- `apply_guess` with a wrong letter increments `wrong` by exactly 1.
- `apply_guess` with a duplicate letter does not change `wrong` (and the
  caller can detect duplicates by comparing state).
- `is_won` is true iff every letter of `word` is in `guessed`.
- `is_lost` is true iff `wrong >= max_wrong`.
- `render_word` masks unguessed letters as `_` and preserves guessed ones.

## Definition of done

- `make` from `tuicade/` passes (ruff, basedpyright, codespell, pytest).
- `uv run tuicade` lists Hangman in the menu and the game is playable end to
  end.
- One or two commits, PR titled `feat: hangman game`.
