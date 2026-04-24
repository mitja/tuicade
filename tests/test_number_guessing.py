import random

from tuicade.games.number_guessing import SECRET_MAX, SECRET_MIN, evaluate_guess, pick_secret


def test_evaluate_guess_higher():
    assert evaluate_guess(50, 30) == "higher"


def test_evaluate_guess_lower():
    assert evaluate_guess(50, 70) == "lower"


def test_evaluate_guess_correct():
    assert evaluate_guess(50, 50) == "correct"


def test_evaluate_guess_boundary_min():
    assert evaluate_guess(1, 1) == "correct"
    assert evaluate_guess(1, 2) == "lower"


def test_evaluate_guess_boundary_max():
    assert evaluate_guess(100, 100) == "correct"
    assert evaluate_guess(100, 99) == "higher"


def test_pick_secret_in_range():
    for seed in range(20):
        rng = random.Random(seed)
        secret = pick_secret(rng)
        assert SECRET_MIN <= secret <= SECRET_MAX, (
            f"pick_secret returned {secret!r} out of [{SECRET_MIN}, {SECRET_MAX}] with seed={seed}"
        )


def test_pick_secret_determinism():
    rng1 = random.Random(42)
    rng2 = random.Random(42)
    assert pick_secret(rng1) == pick_secret(rng2)


def test_pick_secret_variety():
    """Different seeds should not always produce the same number."""
    results = {pick_secret(random.Random(s)) for s in range(50)}
    assert len(results) > 1, "pick_secret produced the same number for all seeds"
