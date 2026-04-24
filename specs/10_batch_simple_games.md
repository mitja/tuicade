# Spec 10 — Batch: three simple games via automatic parallelization

**Prerequisite:** Spec `00_launcher.md` has been merged.

**Recommended model:** Claude Opus 4.7 for the coordinator. Plan mode **on**
for the first turn so the user can see and approve the dispatch plan before
work starts. Subagents: invoke via Claude Code's `Agent` tool with
`subagent_type: "general-purpose"` and `model: "sonnet"` (tight scope,
mechanical).

**Why this is one spec instead of three:** the three games below are tiny
and uniform — almost the same shape. Fanning out to three subagents in one
message shows off the "automatic parallelization" pattern without adding
coordination overhead.

## Your role (coordinator)

1. **Plan.** Read this spec and confirm the three subagent prompts you will
   dispatch. Produce a short plan and wait for approval (plan mode).
2. **Dispatch in parallel.** Send a single assistant message containing
   three `Agent` tool calls — one per game below. Each subagent gets the
   full text of its sub-spec section from this file, plus a reminder that
   it must only edit the two files listed for its game.
3. **Reconcile.** After all three subagents return, run `make` once from
   the `tuicade/` root. Report back per game: file paths created, test
   count, pass/fail.
4. **PR.** Create a single PR titled
   `feat: number guessing, dice roll, rock-paper-scissors` covering all
   three games. Do not split into three PRs — the point of this pattern is
   a single batched result.

## Shared rules for every subagent

- Follow the shared contract from `src/tuicade/launcher.py` (import `Game`,
  expose a module-level `GAME`).
- Only edit the two files listed in your sub-spec. Do not touch
  `launcher.py`, `pyproject.toml`, or any other game's files.
- Use `rich==15.0.0` (already pinned in `pyproject.toml`) for any coloured
  or panelled output. Do not add new dependencies.
- Include `q` as a quit-to-launcher shortcut inside the game loop.
- Tests cover pure logic only, not interactive loops.
- Accept a seeded `random.Random` where randomness matters, so tests are
  deterministic.

## Subagent A — Number Guessing

**Files:** `src/tuicade/games/number_guessing.py`,
`tests/test_number_guessing.py`.

**Gameplay:** Computer picks an integer in `[1, 100]`. Player guesses.
After each guess the game says `higher`, `lower`, or `correct`. Max 7
attempts. On exhaust, reveal the number in red.

**Pure logic to export and test:**

```python
def evaluate_guess(secret: int, guess: int) -> Literal["higher", "lower", "correct"]: ...
```

- `evaluate_guess(50, 30) == "higher"`
- `evaluate_guess(50, 70) == "lower"`
- `evaluate_guess(50, 50) == "correct"`

**`GAME` descriptor:** slug `number_guessing`, title `Number Guessing`,
description `Guess the secret number (1-100) in 7 tries.`

## Subagent B — Dice Roll Simulator

**Files:** `src/tuicade/games/dice_roll.py`, `tests/test_dice_roll.py`.

**Gameplay:** Prompt loop accepting dice notation. Examples: `d20`, `2d6`,
`3d8+2`, `4d6-1`. Show per-die results and the total, formatted with rich
(e.g. a small table or panel). `q` quits.

**Pure logic to export and test:**

```python
@dataclass(frozen=True)
class DiceNotation:
    count: int       # default 1 when notation is like "d20"
    sides: int
    modifier: int    # default 0

def parse_notation(s: str) -> DiceNotation: ...  # raises ValueError on bad input
def roll(notation: DiceNotation, rng: random.Random) -> tuple[list[int], int]:
    """Return (per-die results, total including modifier)."""
```

Tests:

- `parse_notation("d20")` → `DiceNotation(1, 20, 0)`.
- `parse_notation("2d6")` → `DiceNotation(2, 6, 0)`.
- `parse_notation("3d8+2")` → `DiceNotation(3, 8, 2)`.
- `parse_notation("4d6-1")` → `DiceNotation(4, 6, -1)`.
- `parse_notation("nonsense")` raises `ValueError`.
- `roll` with fixed seed is deterministic; `len(dice) == count`; every die
  ∈ `[1, sides]`; `sum(dice) + modifier == total`.

**`GAME` descriptor:** slug `dice_roll`, title `Dice Roll`, description
`Roll any dice notation like 2d6 or 3d8+2.`

## Subagent C — Rock-Paper-Scissors

**Files:** `src/tuicade/games/rock_paper_scissors.py`,
`tests/test_rock_paper_scissors.py`.

**Gameplay:** Best-of-3 against the computer (computer uses a seeded
`random.Random`). Show running score after each round. Declare match
winner at the end.

**Pure logic to export and test:**

```python
Move = Literal["rock", "paper", "scissors"]
Outcome = Literal["win", "lose", "tie"]

def decide(player: Move, computer: Move) -> Outcome: ...
```

Tests: exhaustively cover all 9 (player, computer) combinations.

**`GAME` descriptor:** slug `rock_paper_scissors`, title `Rock-Paper-Scissors`,
description `Best of three vs. the computer.`

## Definition of done (coordinator)

- All three subagents completed successfully.
- `make` passes from `tuicade/`.
- `uv run tuicade` lists six games total (three from this PR + the three
  from the manual-parallel specs + Hangman/Tic-Tac-Toe/Word Scramble).
- One PR covers all three games.
