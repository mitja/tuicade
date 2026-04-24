from __future__ import annotations

import pytest

from tuicade.games.rock_paper_scissors import Move, Outcome, decide

# ---------------------------------------------------------------------------
# Exhaustive coverage of all 9 (player, computer) combinations
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("player", "computer", "expected"),
    [
        # Ties
        ("rock", "rock", "tie"),
        ("paper", "paper", "tie"),
        ("scissors", "scissors", "tie"),
        # Player wins
        ("rock", "scissors", "win"),
        ("paper", "rock", "win"),
        ("scissors", "paper", "win"),
        # Player loses
        ("rock", "paper", "lose"),
        ("paper", "scissors", "lose"),
        ("scissors", "rock", "lose"),
    ],
)
def test_decide_all_combinations(player: Move, computer: Move, expected: Outcome) -> None:
    assert decide(player, computer) == expected


# ---------------------------------------------------------------------------
# Additional property checks
# ---------------------------------------------------------------------------


def test_decide_returns_tie_for_same_move() -> None:
    for move in ("rock", "paper", "scissors"):
        m: Move = move  # type: ignore[assignment]
        assert decide(m, m) == "tie"


def test_decide_win_lose_are_symmetric() -> None:
    """If player wins with (a, b), computer wins means decide(b, a) == 'lose'."""
    pairs: list[tuple[Move, Move]] = [
        ("rock", "scissors"),
        ("paper", "rock"),
        ("scissors", "paper"),
    ]
    for player, computer in pairs:
        assert decide(player, computer) == "win"
        assert decide(computer, player) == "lose"
