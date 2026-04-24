from __future__ import annotations

from tuicade.games.hangman import (
    HangmanState,
    apply_guess,
    is_lost,
    is_won,
    render_word,
)


def test_apply_guess_correct_letter() -> None:
    state = HangmanState(word="cat")
    new_state = apply_guess(state, "c")
    assert "c" in new_state.guessed
    assert new_state.wrong == 0


def test_apply_guess_wrong_letter() -> None:
    state = HangmanState(word="cat")
    new_state = apply_guess(state, "z")
    assert new_state.wrong == 1


def test_apply_guess_duplicate_letter_does_not_increment_wrong() -> None:
    state = HangmanState(word="cat", guessed={"z"}, wrong=1)
    new_state = apply_guess(state, "z")
    assert new_state.wrong == 1
    assert new_state is state  # no change — returns same object


def test_apply_guess_duplicate_correct_letter() -> None:
    state = HangmanState(word="cat", guessed={"c"}, wrong=0)
    new_state = apply_guess(state, "c")
    assert new_state is state


def test_is_won_true() -> None:
    state = HangmanState(word="cat", guessed={"c", "a", "t"})
    assert is_won(state) is True


def test_is_won_false_missing_letter() -> None:
    state = HangmanState(word="cat", guessed={"c", "a"})
    assert is_won(state) is False


def test_is_lost_true() -> None:
    state = HangmanState(word="cat", wrong=6)
    assert is_lost(state) is True


def test_is_lost_false() -> None:
    state = HangmanState(word="cat", wrong=5)
    assert is_lost(state) is False


def test_is_lost_custom_max_wrong() -> None:
    state = HangmanState(word="cat", wrong=3)
    assert is_lost(state, max_wrong=3) is True
    assert is_lost(state, max_wrong=4) is False


def test_render_word_all_masked() -> None:
    state = HangmanState(word="cat")
    assert render_word(state) == "_ _ _"


def test_render_word_partial() -> None:
    state = HangmanState(word="cat", guessed={"c", "t"})
    assert render_word(state) == "c _ t"


def test_render_word_fully_revealed() -> None:
    state = HangmanState(word="cat", guessed={"c", "a", "t"})
    assert render_word(state) == "c a t"
