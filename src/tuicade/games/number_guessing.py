from __future__ import annotations

import random
from typing import Literal

from rich.console import Console

from tuicade.launcher import Game

MAX_ATTEMPTS = 7
SECRET_MIN = 1
SECRET_MAX = 100


def pick_secret(rng: random.Random) -> int:
    """Pick a secret integer in [SECRET_MIN, SECRET_MAX] using the given rng."""
    return rng.randint(SECRET_MIN, SECRET_MAX)


def evaluate_guess(secret: int, guess: int) -> Literal["higher", "lower", "correct"]:
    """Return 'higher' if the secret is higher than the guess, 'lower' if it's lower,
    or 'correct' if they match."""
    if guess < secret:
        return "higher"
    if guess > secret:
        return "lower"
    return "correct"


def play() -> None:
    console = Console()
    rng = random.Random()
    secret = pick_secret(rng)
    attempts_left = MAX_ATTEMPTS

    while True:
        console.clear()
        console.print("[bold magenta]Number Guessing[/bold magenta]")
        console.print()
        console.print(
            f"Guess a number between [bold]{SECRET_MIN}[/bold] and [bold]{SECRET_MAX}[/bold]."
        )
        console.print(f"Attempts left: [bold]{attempts_left}[/bold]")
        console.print()
        console.print("[dim]Enter a number, or [bold]q[/bold] to quit.[/dim]")

        raw = console.input("Guess: ").strip()

        if raw.lower() == "q":
            return

        if not raw.isdigit() and not (raw.startswith("-") and raw[1:].isdigit()):
            console.print("[yellow]Please enter a valid integer.[/yellow]")
            console.input("Press Enter to try again…")
            continue

        guess = int(raw)
        result = evaluate_guess(secret, guess)

        if result == "correct":
            console.print(
                f"\n[bold green]Correct![/bold green] The number was: [bold]{secret}[/bold]"
            )
            console.input("\nPress Enter to continue…")
            return

        attempts_left -= 1

        if attempts_left == 0:
            console.print(f"\n[bold red]Out of attempts! The number was: {secret}[/bold red]")
            console.input("\nPress Enter to continue…")
            return

        hint = "Go [bold]higher[/bold]!" if result == "higher" else "Go [bold]lower[/bold]!"
        console.print(
            f"\n[yellow]{hint} {attempts_left} attempt{'s' if attempts_left != 1 else ''} remaining.[/yellow]"
        )
        console.input("Press Enter to try again…")


GAME = Game(
    slug="number_guessing",
    title="Number Guessing",
    description="Guess the secret number (1-100) in 7 tries.",
    run=play,
)
