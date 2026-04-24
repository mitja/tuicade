import random

from tuicade.games.word_scramble import WORDS, check_guess, scramble


def test_scramble_never_equals_original_for_multi_distinct_letters():
    """scramble never returns the original word for words with >=2 distinct letters."""
    words_with_distinct = [w for w in WORDS if len({ch for ch in w if ch != "-"}) >= 2]
    for seed in range(5):
        rng = random.Random(seed)
        for word in words_with_distinct:
            result = scramble(word, rng)
            assert result != word, f"scramble({word!r}, seed={seed}) returned the original"


def test_scramble_preserves_letter_multiset():
    """scramble preserves the multiset of letters (sorted letters match)."""
    for seed in range(5):
        rng = random.Random(seed)
        for word in WORDS:
            result = scramble(word, rng)
            orig_letters = sorted(ch for ch in word if ch != "-")
            result_letters = sorted(ch for ch in result if ch != "-")
            assert orig_letters == result_letters, (
                f"Letter multiset changed: {word!r} -> {result!r}"
            )


def test_scramble_fine_tuning_keeps_hyphen_at_index_4():
    """scramble('fine-tuning', rng) keeps the hyphen at index 4."""
    for seed in range(5):
        rng = random.Random(seed)
        result = scramble("fine-tuning", rng)
        assert result[4] == "-", f"Hyphen moved in {result!r} (seed={seed})"


def test_scramble_determinism():
    """Same rng seed produces the same scramble."""
    for word in WORDS:
        result1 = scramble(word, random.Random(42))
        result2 = scramble(word, random.Random(42))
        assert result1 == result2, f"Non-deterministic for {word!r}"


def test_check_guess_case_insensitive():
    assert check_guess("PROMPT", "prompt") is True
    assert check_guess("prompt", "PROMPT") is True


def test_check_guess_ignores_whitespace():
    assert check_guess("prompt", "  Prompt ") is True
    assert check_guess("  Prompt ", "prompt") is True


def test_check_guess_mismatch():
    assert check_guess("prompt", "context") is False
    assert check_guess("agent", "agents") is False
