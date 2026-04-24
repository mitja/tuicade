from __future__ import annotations

import random
from dataclasses import dataclass, field

from rich.console import Console

from tuicade.launcher import Game

WORDS = [
    "transformer",
    "embedding",
    "gradient",
    "tokenizer",
    "attention",
    "softmax",
    "backprop",
    "perceptron",
    "dropout",
    "activation",
    "convolution",
    "recurrence",
    "sampler",
    "logits",
    "dataset",
    "epoch",
    "checkpoint",
    "inference",
    "prompt",
    "context",
]

_GALLOWS = [
    # 0 wrong
    [
        "  +---+",
        "  |   |",
        "      |",
        "      |",
        "      |",
        "      |",
        "=========",
    ],
    # 1 wrong — head
    [
        "  +---+",
        "  |   |",
        "  O   |",
        "      |",
        "      |",
        "      |",
        "=========",
    ],
    # 2 wrong — body
    [
        "  +---+",
        "  |   |",
        "  O   |",
        "  |   |",
        "      |",
        "      |",
        "=========",
    ],
    # 3 wrong — left arm
    [
        "  +---+",
        "  |   |",
        "  O   |",
        " /|   |",
        "      |",
        "      |",
        "=========",
    ],
    # 4 wrong — both arms
    [
        "  +---+",
        "  |   |",
        "  O   |",
        " /|\\  |",
        "      |",
        "      |",
        "=========",
    ],
    # 5 wrong — left leg
    [
        "  +---+",
        "  |   |",
        "  O   |",
        " /|\\  |",
        " /    |",
        "      |",
        "=========",
    ],
    # 6 wrong — both legs (game over)
    [
        "  +---+",
        "  |   |",
        "  O   |",
        " /|\\  |",
        " / \\  |",
        "      |",
        "=========",
    ],
]


@dataclass
class HangmanState:
    word: str
    guessed: set[str] = field(default_factory=set)
    wrong: int = 0


def apply_guess(state: HangmanState, letter: str) -> HangmanState:
    """Return a new state after applying *letter*. Duplicates are a no-op."""
    if letter in state.guessed:
        return state
    new_guessed = state.guessed | {letter}
    new_wrong = state.wrong if letter in state.word else state.wrong + 1
    return HangmanState(word=state.word, guessed=new_guessed, wrong=new_wrong)


def is_won(state: HangmanState) -> bool:
    return all(ch in state.guessed for ch in state.word)


def is_lost(state: HangmanState, max_wrong: int = 6) -> bool:
    return state.wrong >= max_wrong


def render_word(state: HangmanState) -> str:
    return " ".join(ch if ch in state.guessed else "_" for ch in state.word)


def play() -> None:
    console = Console()
    word = random.choice(WORDS)
    state = HangmanState(word=word)
    max_wrong = 6

    while True:
        console.clear()

        # Gallows
        stage = min(state.wrong, max_wrong)
        color = "red" if stage == max_wrong else "yellow"
        for line in _GALLOWS[stage]:
            console.print(f"[{color}]{line}[/{color}]")

        console.print()
        console.print(f"[bold]{render_word(state)}[/bold]")
        console.print()

        guessed_sorted = ", ".join(sorted(state.guessed)) if state.guessed else "—"
        console.print(f"Guessed: [cyan]{guessed_sorted}[/cyan]")
        console.print(f"Wrong guesses left: [bold]{max_wrong - state.wrong}[/bold]")
        console.print()

        if is_won(state):
            console.print(
                f"[bold green]You saved them![/bold green] The word was: [bold]{word}[/bold]"
            )
            console.input("\nPress Enter to continue…")
            return

        if is_lost(state, max_wrong):
            console.print(f"[bold red]You lost — the word was: {word}[/bold red]")
            console.input("\nPress Enter to continue…")
            return

        console.print("[dim]Enter a letter, or [bold]q[/bold] to quit.[/dim]")
        raw = console.input("Guess: ").strip().lower()

        if raw == "q":
            return

        if len(raw) != 1 or not raw.isalpha():
            console.print("[yellow]Please enter a single letter.[/yellow]")
            console.input("Press Enter…")
            continue

        if raw in state.guessed:
            console.print(f"[yellow]You already guessed '{raw}'. Try another letter.[/yellow]")
            console.input("Press Enter…")
            continue

        new_state = apply_guess(state, raw)
        if raw in state.word:
            console.print(f"[green]'{raw}' is in the word![/green]")
        else:
            console.print(f"[red]'{raw}' is not in the word.[/red]")
        state = new_state


GAME = Game(
    slug="hangman",
    title="Hangman",
    description="Guess the AI/ML word before the stickman falls.",
    run=play,
)
