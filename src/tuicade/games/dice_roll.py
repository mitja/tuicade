from __future__ import annotations

import random
import re
from dataclasses import dataclass

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from tuicade.launcher import Game

_NOTATION_RE = re.compile(r"^\s*(?P<count>\d+)?\s*[dD](?P<sides>\d+)\s*(?P<mod>[+-]\s*\d+)?\s*$")


@dataclass(frozen=True)
class DiceNotation:
    count: int  # default 1 when notation is like "d20"
    sides: int
    modifier: int  # default 0


def parse_notation(s: str) -> DiceNotation:
    """Parse a dice notation string into a DiceNotation. Raises ValueError on bad input."""
    m = _NOTATION_RE.match(s)
    if m is None:
        raise ValueError(f"Invalid dice notation: {s!r}")

    count_str = m.group("count")
    sides_str = m.group("sides")
    mod_str = m.group("mod")

    count = int(count_str) if count_str is not None else 1
    sides = int(sides_str)
    modifier = int(mod_str.replace(" ", "")) if mod_str is not None else 0

    if count < 1:
        raise ValueError(f"Dice count must be >= 1, got {count}")
    if sides < 1:
        raise ValueError(f"Dice sides must be >= 1, got {sides}")

    return DiceNotation(count=count, sides=sides, modifier=modifier)


def roll(notation: DiceNotation, rng: random.Random) -> tuple[list[int], int]:
    """Return (per-die results, total including modifier)."""
    dice = [rng.randint(1, notation.sides) for _ in range(notation.count)]
    total = sum(dice) + notation.modifier
    return dice, total


def play() -> None:
    console = Console()
    rng = random.Random()

    console.print(
        Panel(
            "[bold cyan]Dice Roll Simulator[/bold cyan]\n"
            "[dim]Enter dice notation like [bold]d20[/bold], [bold]2d6[/bold], "
            "[bold]3d8+2[/bold], or [bold]4d6-1[/bold].[/dim]\n"
            "[dim]Type [bold]q[/bold] to quit.[/dim]",
            expand=False,
        )
    )

    while True:
        raw = console.input("\n[bold]Notation:[/bold] ").strip()

        if raw.lower() == "q":
            return

        if not raw:
            continue

        try:
            notation = parse_notation(raw)
        except ValueError as exc:
            console.print(f"[red]Error:[/red] {exc}")
            continue

        dice, total = roll(notation, rng)

        table = Table(show_header=True, header_style="bold magenta", expand=False)
        table.add_column("Die", style="dim", width=6)
        table.add_column("Result", justify="right")

        for i, value in enumerate(dice, start=1):
            table.add_row(f"d{notation.sides} #{i}", str(value))

        if notation.modifier != 0:
            sign = "+" if notation.modifier > 0 else ""
            table.add_row("[dim]Modifier[/dim]", f"{sign}{notation.modifier}")

        table.add_row("[bold]Total[/bold]", f"[bold green]{total}[/bold green]")

        console.print(table)


GAME = Game(
    slug="dice_roll",
    title="Dice Roll",
    description="Roll any dice notation like 2d6 or 3d8+2.",
    run=play,
)
