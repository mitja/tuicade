from __future__ import annotations

import random

import pytest

from tuicade.games.dice_roll import DiceNotation, parse_notation, roll


def test_parse_notation_d20():
    assert parse_notation("d20") == DiceNotation(1, 20, 0)


def test_parse_notation_2d6():
    assert parse_notation("2d6") == DiceNotation(2, 6, 0)


def test_parse_notation_3d8_plus_2():
    assert parse_notation("3d8+2") == DiceNotation(3, 8, 2)


def test_parse_notation_4d6_minus_1():
    assert parse_notation("4d6-1") == DiceNotation(4, 6, -1)


def test_parse_notation_nonsense_raises():
    with pytest.raises(ValueError):
        parse_notation("nonsense")


def test_parse_notation_missing_d_raises():
    with pytest.raises(ValueError):
        parse_notation("206")


def test_parse_notation_empty_raises():
    with pytest.raises(ValueError):
        parse_notation("")


def test_parse_notation_uppercase_d():
    assert parse_notation("D20") == DiceNotation(1, 20, 0)


def test_parse_notation_uppercase_2d6():
    assert parse_notation("2D6") == DiceNotation(2, 6, 0)


def test_parse_notation_trailing_junk_raises():
    with pytest.raises(ValueError):
        parse_notation("2d6abc")


def test_roll_deterministic():
    notation = DiceNotation(3, 6, 0)
    rng1 = random.Random(42)
    rng2 = random.Random(42)
    dice1, total1 = roll(notation, rng1)
    dice2, total2 = roll(notation, rng2)
    assert dice1 == dice2
    assert total1 == total2


def test_roll_count_matches():
    notation = DiceNotation(4, 6, 0)
    rng = random.Random(99)
    dice, _ = roll(notation, rng)
    assert len(dice) == 4


def test_roll_die_values_in_range():
    notation = DiceNotation(10, 8, 0)
    rng = random.Random(7)
    dice, _ = roll(notation, rng)
    for value in dice:
        assert 1 <= value <= 8


def test_roll_total_includes_modifier():
    notation = DiceNotation(3, 8, 2)
    rng = random.Random(13)
    dice, total = roll(notation, rng)
    assert sum(dice) + notation.modifier == total


def test_roll_total_with_negative_modifier():
    notation = DiceNotation(4, 6, -1)
    rng = random.Random(21)
    dice, total = roll(notation, rng)
    assert sum(dice) + notation.modifier == total


def test_roll_single_die_no_modifier():
    notation = DiceNotation(1, 20, 0)
    rng = random.Random(0)
    dice, total = roll(notation, rng)
    assert len(dice) == 1
    assert 1 <= dice[0] <= 20
    assert total == dice[0]
