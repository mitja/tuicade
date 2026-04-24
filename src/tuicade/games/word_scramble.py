from __future__ import annotations

import random

from rich.console import Console

from tuicade.launcher import Game

WORDS: tuple[str, ...] = (
    "prompt",
    "context",
    "tokenizer",
    "embedding",
    "retrieval",
    "agent",
    "inference",
    "hallucination",
    "temperature",
    "grounding",
    "evaluation",
    "benchmark",
    "guardrail",
    "latency",
    "throughput",
    "distillation",
    "quantization",
    "rag",
    "multimodal",
    "fine-tuning",
)

MAX_ATTEMPTS = 3


def scramble(word: str, rng: random.Random, max_tries: int = 20) -> str:
    """Return a scrambled form of *word*. Hyphen stays in place. Result is
    guaranteed not equal to the input unless the word has <2 distinct
    letters; in that case the original is returned."""
    # Collect only letter characters and their original positions
    letter_indices = [i for i, ch in enumerate(word) if ch != "-"]
    letters = [word[i] for i in letter_indices]

    if len(set(letters)) < 2:
        return word

    shuffled = letters[:]
    for _ in range(max_tries):
        rng.shuffle(shuffled)
        if shuffled != letters:
            break

    # Reconstruct word with hyphens restored
    result = list(word)
    for idx, ch in zip(letter_indices, shuffled, strict=True):
        result[idx] = ch
    return "".join(result)


def check_guess(word: str, guess: str) -> bool:
    """Case- and whitespace-insensitive equality."""
    return word.strip().casefold() == guess.strip().casefold()


def play() -> None:
    console = Console()
    rng = random.Random()
    word = rng.choice(WORDS)
    scrambled = scramble(word, rng)
    attempts_left = MAX_ATTEMPTS

    while True:
        console.clear()
        console.print("[bold magenta]Word Scramble[/bold magenta]")
        console.print()
        console.print(
            f"Unscramble: [bold yellow]{scrambled}[/bold yellow]  [dim](AI engineering term)[/dim]"
        )
        console.print(f"Attempts left: [bold]{attempts_left}[/bold]")
        console.print()
        console.print("[dim]Type your answer, or [bold]q[/bold] to quit.[/dim]")

        raw = console.input("Guess: ").strip()

        if raw.lower() == "q":
            return

        if check_guess(word, raw):
            console.print(f"\n[bold green]Correct![/bold green] The word was: [bold]{word}[/bold]")
            console.input("\nPress Enter to continue…")
            return

        attempts_left -= 1
        if attempts_left == 0:
            console.print(f"\n[bold red]Out of attempts! The word was: {word}[/bold red]")
            console.input("\nPress Enter to continue…")
            return

        console.print(
            f"\n[yellow]Wrong! {attempts_left} attempt{'s' if attempts_left != 1 else ''} remaining.[/yellow]"
        )
        console.input("Press Enter to try again…")


GAME = Game(
    slug="word_scramble",
    title="Word Scramble",
    description="Unscramble an AI engineering term in 3 tries.",
    run=play,
)
