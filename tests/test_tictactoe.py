from __future__ import annotations

import random

import pytest

from tuicade.games.tictactoe import (
    apply_move,
    available_moves,
    check_winner,
    computer_move,
)

# ---------------------------------------------------------------------------
# check_winner
# ---------------------------------------------------------------------------


def _board(s: str) -> list:
    """Build a Board from a 9-char string of X, O, or space."""
    return list(s)


@pytest.mark.parametrize(
    "layout,expected",
    [
        # X wins — rows
        ("XXX      ", "X"),
        ("   XXX   ", "X"),
        ("      XXX", "X"),
        # X wins — columns
        ("X  X  X  ", "X"),
        (" X  X  X ", "X"),
        ("  X  X  X", "X"),
        # X wins — diagonals
        ("X   X   X", "X"),
        ("  X X X  ", "X"),
        # O wins — row
        ("OOO      ", "O"),
        # O wins — column
        ("O  O  O  ", "O"),
        # O wins — diagonal
        ("O   O   O", "O"),
        # No winner yet
        ("XO XO    ", None),
        # Full draw board
        ("XOXOXOOXO", None),  # no winner despite full board (drawn)
        # Empty board
        ("         ", None),
    ],
)
def test_check_winner(layout: str, expected):
    board = _board(layout)
    assert check_winner(board) == expected


# ---------------------------------------------------------------------------
# available_moves
# ---------------------------------------------------------------------------


def test_available_moves_empty_board():
    board = _board("         ")
    assert available_moves(board) == list(range(9))


def test_available_moves_full_board():
    board = _board("XOXOXOOXO")
    assert available_moves(board) == []


def test_available_moves_partial():
    board = _board("XO  X    ")
    result = available_moves(board)
    # indices 2,3,5,6,7,8 are empty
    assert result == [2, 3, 5, 6, 7, 8]
    assert len(result) == 6


# ---------------------------------------------------------------------------
# computer_move
# ---------------------------------------------------------------------------

_RNG = random.Random(42)


def test_computer_move_takes_win():
    # O can win by playing index 2 (row 0)
    board = _board("OO  X X  ")
    move = computer_move(board, _RNG)
    assert move == 2


def test_computer_move_blocks_x():
    # X can win by playing index 2; O has no immediate win
    board = _board("XX  O    ")
    move = computer_move(board, _RNG)
    assert move == 2


def test_computer_move_prefers_center():
    board = _board("         ")
    move = computer_move(board, _RNG)
    assert move == 4


def test_computer_move_deterministic():
    board = _board("X        ")
    rng1 = random.Random(0)
    rng2 = random.Random(0)
    assert computer_move(board, rng1) == computer_move(board, rng2)


def test_computer_move_takes_corner_when_no_center():
    # Center is taken; O should prefer a corner
    board = _board("    X    ")
    move = computer_move(board, random.Random(7))
    assert move in (0, 2, 6, 8)


# ---------------------------------------------------------------------------
# apply_move
# ---------------------------------------------------------------------------


def test_apply_move_returns_new_board():
    board = _board("         ")
    new_board = apply_move(board, 4, "X")
    assert new_board[4] == "X"
    assert board[4] == " "  # original unchanged
