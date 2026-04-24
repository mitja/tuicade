from __future__ import annotations

import random
from typing import Literal

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from tuicade.launcher import Game

Cell = Literal["X", "O", " "]
Board = list[Cell]  # length 9

# Numpad layout -> list index:
#  7 | 8 | 9      0 | 1 | 2
#  4 | 5 | 6  ->  3 | 4 | 5
#  1 | 2 | 3      6 | 7 | 8
_NUMPAD_TO_IDX: dict[int, int] = {7: 0, 8: 1, 9: 2, 4: 3, 5: 4, 6: 5, 1: 6, 2: 7, 3: 8}

_WIN_LINES: list[tuple[int, int, int]] = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
]

_CORNERS: list[int] = [0, 2, 6, 8]
_SIDES: list[int] = [1, 3, 5, 7]


def check_winner(board: Board) -> Cell | None:
    """Return 'X', 'O', or None."""
    for a, b, c in _WIN_LINES:
        if board[a] != " " and board[a] == board[b] == board[c]:
            return board[a]  # type: ignore[return-value]
    return None


def available_moves(board: Board) -> list[int]:
    """Return list indices that are empty."""
    return [i for i, cell in enumerate(board) if cell == " "]


def computer_move(board: Board, rng: random.Random) -> int:
    """Return the best list index for O to play."""
    moves = available_moves(board)

    # 1. Win if possible
    for idx in moves:
        board[idx] = "O"
        if check_winner(board) == "O":
            board[idx] = " "
            return idx
        board[idx] = " "

    # 2. Block X from winning
    for idx in moves:
        board[idx] = "X"
        if check_winner(board) == "X":
            board[idx] = " "
            return idx
        board[idx] = " "

    # 3. Center
    if 4 in moves:
        return 4

    # 4. Any free corner
    corners = [i for i in _CORNERS if i in moves]
    if corners:
        return rng.choice(corners)

    # 5. Any free side
    sides = [i for i in _SIDES if i in moves]
    if sides:
        return rng.choice(sides)

    return moves[0]  # fallback (shouldn't be reached)


def apply_move(board: Board, idx: int, mark: Cell) -> Board:
    """Return a new board with the move applied."""
    new_board: Board = board.copy()
    new_board[idx] = mark
    return new_board


def _render_board(board: Board) -> str:
    """Render the board as a string with numpad hints."""
    _idx_to_num = {v: k for k, v in _NUMPAD_TO_IDX.items()}

    def cell(i: int) -> str:
        return board[i] if board[i] != " " else str(_idx_to_num[i])

    rows = [
        f" {cell(0)} | {cell(1)} | {cell(2)} ",
        "---+---+---",
        f" {cell(3)} | {cell(4)} | {cell(5)} ",
        "---+---+---",
        f" {cell(6)} | {cell(7)} | {cell(8)} ",
    ]
    return "\n".join(rows)


def play() -> None:
    console = Console()
    rng = random.Random()
    board: Board = [" "] * 9

    while True:
        console.clear()
        console.print(Panel(_render_board(board), title="Tic-Tac-Toe", expand=False))
        console.print(
            "[dim]You are [bold]X[/bold]. Enter a numpad key (1-9) or [bold]q[/bold] to quit.[/dim]"
        )

        winner = check_winner(board)
        moves = available_moves(board)

        if winner or not moves:
            if winner == "X":
                msg = "[bold green]You win! 🎉[/bold green]"
            elif winner == "O":
                msg = "[bold red]Computer wins![/bold red]"
            else:
                msg = "[bold yellow]It's a draw![/bold yellow]"
            console.print(Panel(msg, expand=False))
            Prompt.ask("Press Enter to return to the launcher", console=console, default="")
            return

        raw = Prompt.ask("Your move", console=console, default="q")
        if raw.strip().lower() == "q":
            return

        if not raw.strip().isdigit() or int(raw.strip()) not in _NUMPAD_TO_IDX:
            console.print("[red]Invalid key. Use 1–9.[/red]")
            Prompt.ask("Press Enter to continue", console=console, default="")
            continue

        idx = _NUMPAD_TO_IDX[int(raw.strip())]
        if board[idx] != " ":
            console.print("[red]That cell is already taken.[/red]")
            Prompt.ask("Press Enter to continue", console=console, default="")
            continue

        board = apply_move(board, idx, "X")

        winner = check_winner(board)
        moves = available_moves(board)
        if winner or not moves:
            continue  # loop back to show result

        cpu_idx = computer_move(board, rng)
        board = apply_move(board, cpu_idx, "O")


GAME = Game(
    slug="tictactoe",
    title="Tic-Tac-Toe",
    description="Beat the tiny rule-based bot on a 3x3 grid.",
    run=play,
)
