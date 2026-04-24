# Spec 03 — Word Scramble (AI-engineering terms)

**Prerequisite:** Spec `00_launcher.md` has been merged.

**Recommended model:** Claude Sonnet 4.6. Agent mode.

**Parallel-safe:** Yes. Touches only the two files below.

## Goal

Add a Word Scramble game whose word pool is AI-engineering vocabulary.

## Files you will create

- `src/tuicade/games/word_scramble.py`
- `tests/test_word_scramble.py`

No other file may be edited.

## Word list (use this exact set)

```
prompt, context, tokenizer, embedding, retrieval, agent, inference,
hallucination, temperature, grounding, evaluation, benchmark, guardrail,
latency, throughput, distillation, quantization, rag, multimodal,
fine-tuning
```

Hyphenated entries (`fine-tuning`) keep the hyphen in the rendered output
but are scrambled letter-by-letter ignoring the hyphen — the hyphen is
restored at its original position after scrambling.

## Gameplay

- Pick a random word. Scramble its letters. Show the scrambled form and a
  short hint: "(AI engineering term)".
- Player has **3** attempts. After each wrong guess, show how many remain.
- Guess checking is case-insensitive and ignores surrounding whitespace.
- On success: green "Correct!" + original word. On failure after 3 tries:
  reveal the word in red.
- `q` quits back to the launcher.

## Shape of the code

```python
# src/tuicade/games/word_scramble.py
import random
from tuicade.launcher import Game

WORDS: tuple[str, ...] = (
    "prompt", "context", "tokenizer", "embedding", "retrieval", "agent",
    "inference", "hallucination", "temperature", "grounding", "evaluation",
    "benchmark", "guardrail", "latency", "throughput", "distillation",
    "quantization", "rag", "multimodal", "fine-tuning",
)

def scramble(word: str, rng: random.Random, max_tries: int = 20) -> str:
    """Return a scrambled form of `word`. Hyphen stays in place. Result is
    guaranteed not equal to the input unless the word has <2 distinct
    letters; in that case the original is returned."""

def check_guess(word: str, guess: str) -> bool:
    """Case- and whitespace-insensitive equality."""

def play() -> None: ...

GAME = Game(
    slug="word_scramble",
    title="Word Scramble",
    description="Unscramble an AI engineering term in 3 tries.",
    run=play,
)
```

## Tests (`tests/test_word_scramble.py`)

- `scramble(word, rng)` never returns `word` itself for every entry in
  `WORDS` with ≥2 distinct letters, across a handful of seeds.
- `scramble` preserves the multiset of letters (sorted letters match).
- `scramble("fine-tuning", rng)` keeps the hyphen at index 4.
- Same `rng` seed → same scramble (determinism).
- `check_guess` is case-insensitive: `check_guess("PROMPT", "prompt")` is
  true; `check_guess("prompt", "  Prompt ")` is true; mismatches are false.

## Definition of done

- `make` passes.
- `uv run tuicade` → Word Scramble is playable.
- PR titled `feat: word scramble (AI terms)`.
