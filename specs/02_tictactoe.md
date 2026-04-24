# Spec 02 — Tic-Tac-Toe

**Prerequisite:** Spec `00_launcher.md` has been merged.

**Recommended model:** Claude Sonnet 4.6. Agent mode.

**Parallel-safe:** Yes. Touches only the two files below.

**Dependencies:** use `rich==15.0.0` (already pinned in `pyproject.toml`
by spec 00). Do not add new dependencies.

## Goal

Add a human-vs-computer Tic-Tac-Toe that plugs into the launcher.

## Files you will create

- `src/tuicade/games/tictactoe.py`
- `tests/test_tictactoe.py`

No other file may be edited.

## Gameplay

- 3×3 board, rendered with `rich`. Use a `rich.table.Table` with borders, or
  a `rich.panel.Panel` containing a hand-drawn grid — pick whichever looks
  cleaner; it just needs to be visually distinct from other games in the
  arcade (Hangman shows gallows art, Word Scramble shows scrambled letters —
  Tic-Tac-Toe should clearly show a grid).
- Cells are addressed with numpad layout:
  ```
   7 | 8 | 9
  ---+---+---
   4 | 5 | 6
  ---+---+---
   1 | 2 | 3
  ```
- Player is `X`, computer is `O`. Player moves first. `q` quits to launcher.
- Computer strategy (simple, deterministic with a seed for tests):
  1. If a winning move exists for `O`, take it.
  2. Else, if `X` has a winning move, block it.
  3. Else, take center if free.
  4. Else, take any free corner.
  5. Else, take any free side.
  Random tie-breaking uses a `random.Random` instance so tests can pin it.
- On win/draw, show a `rich` panel with result, pause for Enter, return.

## Shape of the code

```python
# src/tuicade/games/tictactoe.py
import random
from typing import Literal
from tuicade.launcher import Game

Cell = Literal["X", "O", " "]
Board = list[Cell]  # length 9, numpad index -> list index mapping documented

def check_winner(board: Board) -> Cell | None: ...  # "X", "O", or None
def available_moves(board: Board) -> list[int]: ...
def computer_move(board: Board, rng: random.Random) -> int: ...
def apply_move(board: Board, idx: int, mark: Cell) -> Board: ...

def play() -> None: ...

GAME = Game(
    slug="tictactoe",
    title="Tic-Tac-Toe",
    description="Beat the tiny rule-based bot on a 3x3 grid.",
    run=play,
)
```

## Tests (`tests/test_tictactoe.py`)

- `check_winner` detects all 8 lines, for both `X` and `O`.
- `check_winner` returns `None` on an unfinished or drawn board.
- `available_moves` returns the correct count and indices for several
  hand-crafted boards, including a full board (empty list) and an empty
  board (nine entries).
- `computer_move`:
  - Takes a winning move when available (craft a board where `O` can win).
  - Blocks `X` when `X` is one move from winning and `O` has no immediate
    win.
  - Prefers center on an empty board.
  - Is deterministic given a fixed seed.

## Definition of done

- `make` passes.
- `uv run tuicade` → Tic-Tac-Toe is playable.
- PR titled `feat: tic-tac-toe game`.
