from __future__ import annotations

import sys
import types

import pytest

from tuicade.launcher import Game, discover_games


def _make_game(slug: str = "stub") -> Game:
    return Game(
        slug=slug,
        title=slug.title(),
        description="A stub game for testing.",
        run=lambda: None,
    )


def test_discover_games_empty() -> None:
    assert discover_games() == []


def test_discover_games_finds_stub(monkeypatch: pytest.MonkeyPatch) -> None:
    fake_module = types.ModuleType("tuicade.games.stub")
    fake_module.GAME = _make_game("stub")  # pyright: ignore[reportAttributeAccessIssue]
    monkeypatch.setitem(sys.modules, "tuicade.games.stub", fake_module)

    import pkgutil

    fake_info = pkgutil.ModuleInfo(module_finder=object(), name="tuicade.games.stub", ispkg=False)  # pyright: ignore[reportArgumentType]
    monkeypatch.setattr(
        "tuicade.launcher.pkgutil.iter_modules",
        lambda *_args, **_kwargs: iter([fake_info]),
    )
    monkeypatch.setattr(
        "tuicade.launcher.importlib.import_module",
        lambda name: sys.modules[name],
    )

    games = discover_games()
    assert len(games) == 1
    assert games[0].slug == "stub"


def test_discover_games_skips_module_without_game(monkeypatch: pytest.MonkeyPatch) -> None:
    fake_module = types.ModuleType("tuicade.games.nogame")
    # Intentionally no GAME attribute
    monkeypatch.setitem(sys.modules, "tuicade.games.nogame", fake_module)

    import pkgutil

    fake_info = pkgutil.ModuleInfo(module_finder=object(), name="tuicade.games.nogame", ispkg=False)  # pyright: ignore[reportArgumentType]
    monkeypatch.setattr(
        "tuicade.launcher.pkgutil.iter_modules",
        lambda *_args, **_kwargs: iter([fake_info]),
    )
    monkeypatch.setattr(
        "tuicade.launcher.importlib.import_module",
        lambda name: sys.modules[name],
    )

    games = discover_games()
    assert games == []
