from __future__ import annotations

import importlib
import pkgutil
from collections.abc import Callable
from dataclasses import dataclass

from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table


@dataclass(frozen=True)
class Game:
    slug: str
    title: str
    description: str
    run: Callable[[], None]


def discover_games() -> list[Game]:
    import tuicade.games  # lazy import to avoid circular dependency at package init

    games: list[Game] = []
    console = Console(stderr=True)
    for mod_info in pkgutil.iter_modules(tuicade.games.__path__, prefix="tuicade.games."):
        try:
            module = importlib.import_module(mod_info.name)
        except Exception as exc:
            console.print(f"[yellow]Warning: could not import {mod_info.name}: {exc}[/yellow]")
            continue
        if not hasattr(module, "GAME"):
            console.print(
                f"[yellow]Warning: {mod_info.name} has no GAME attribute — skipping.[/yellow]"
            )
            continue
        games.append(module.GAME)
    games.sort(key=lambda g: g.title.casefold())
    return games


def run_menu(console: Console | None = None) -> None:
    if console is None:
        console = Console()

    while True:
        console.clear()
        games = discover_games()

        table = Table(
            title="tuicade — terminal arcade", show_header=True, header_style="bold magenta"
        )
        table.add_column("#", style="dim", width=4)
        table.add_column("Game")
        table.add_column("What it is")

        if games:
            for i, game in enumerate(games, start=1):
                table.add_row(str(i), game.title, game.description)
        else:
            table.add_row(
                "", "[dim]No games installed yet. Drop a module into src/tuicade/games/.[/dim]", ""
            )

        console.print(table)
        console.print("[dim]Enter a number to play, or [bold]q[/bold] to quit.[/dim]")

        choice = Prompt.ask("Selection", console=console, default="q")

        if choice.strip().lower() == "q":
            break

        if games and choice.strip().isdigit():
            index = int(choice.strip()) - 1
            if 0 <= index < len(games):
                try:
                    games[index].run()
                except KeyboardInterrupt:
                    pass
                continue

        console.print("[red]Invalid selection.[/red]")
        Prompt.ask("Press Enter to continue", console=console, default="")
