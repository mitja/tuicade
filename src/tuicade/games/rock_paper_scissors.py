from __future__ import annotations

import random
from typing import Literal

from rich.console import Console

from tuicade.launcher import Game

Move = Literal["rock", "paper", "scissors"]
Outcome = Literal["win", "lose", "tie"]

_BEATS: dict[Move, Move] = {
    "rock": "scissors",
    "paper": "rock",
    "scissors": "paper",
}

_ALIASES: dict[str, Move] = {
    "r": "rock",
    "p": "paper",
    "s": "scissors",
    "rock": "rock",
    "paper": "paper",
    "scissors": "scissors",
}


def decide(player: Move, computer: Move) -> Outcome:
    """Return the outcome from the player's perspective.

    Args:
        player: The player's move.
        computer: The computer's move.

    Returns:
        "win" if the player wins, "lose" if the computer wins, "tie" if equal.
    """
    if player == computer:
        return "tie"
    if _BEATS[player] == computer:
        return "win"
    return "lose"


def play() -> None:
    """Run a best-of-3 Rock-Paper-Scissors match against the computer.

    Input shortcuts:
        r / rock     — Rock
        p / paper    — Paper
        s / scissors — Scissors
        q            — Quit to launcher
    """
    console = Console()
    rng = random.Random()

    player_wins = 0
    computer_wins = 0
    round_num = 0
    moves: list[Move] = ["rock", "paper", "scissors"]

    while player_wins < 2 and computer_wins < 2 and round_num < 3:
        round_num += 1
        computer_move: Move = rng.choice(moves)

        console.clear()
        console.print("[bold magenta]Rock-Paper-Scissors[/bold magenta]  [dim]Best of 3[/dim]")
        console.print()
        console.print(
            f"Score — You: [bold green]{player_wins}[/bold green]  "
            f"Computer: [bold red]{computer_wins}[/bold red]  "
            f"[dim](Round {round_num})[/dim]"
        )
        console.print()
        console.print(
            "[dim]Enter [bold]r[/bold]ock, [bold]p[/bold]aper, "
            "[bold]s[/bold]cissors, or [bold]q[/bold] to quit.[/dim]"
        )

        raw = console.input("Your move: ").strip().lower()

        if raw == "q":
            return

        player_move = _ALIASES.get(raw)
        if player_move is None:
            console.print("[red]Invalid move. Please enter r, p, s (or full name).[/red]")
            console.input("Press Enter to try again…")
            round_num -= 1  # don't count this as a round
            continue

        outcome = decide(player_move, computer_move)

        console.print()
        console.print(
            f"You chose [bold]{player_move}[/bold], computer chose [bold]{computer_move}[/bold]."
        )

        if outcome == "win":
            player_wins += 1
            console.print("[bold green]You win this round![/bold green]")
        elif outcome == "lose":
            computer_wins += 1
            console.print("[bold red]Computer wins this round![/bold red]")
        else:
            console.print("[yellow]It's a tie — no point awarded.[/yellow]")

        console.print()
        console.print(
            f"Score — You: [bold green]{player_wins}[/bold green]  "
            f"Computer: [bold red]{computer_wins}[/bold red]"
        )
        console.input("\nPress Enter to continue…")

    # Match over — declare winner
    console.clear()
    console.print("[bold magenta]Rock-Paper-Scissors[/bold magenta]  [dim]Match over[/dim]")
    console.print()
    console.print(
        f"Final score — You: [bold green]{player_wins}[/bold green]  "
        f"Computer: [bold red]{computer_wins}[/bold red]"
    )
    console.print()

    if player_wins > computer_wins:
        console.print("[bold green]You win the match! Well played![/bold green]")
    elif computer_wins > player_wins:
        console.print("[bold red]Computer wins the match. Better luck next time![/bold red]")
    else:
        console.print("[yellow]The match is a draw![/yellow]")

    console.input("\nPress Enter to return to the launcher…")


GAME = Game(
    slug="rock_paper_scissors",
    title="Rock-Paper-Scissors",
    description="Best of three vs. the computer.",
    run=play,
)
