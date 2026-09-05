#!/usr/bin/env python3
"""Re-letter options so correct answers are spread evenly across positions.

Deterministic (seeded per question id) so re-runs are stable. Safe only when no
option text / why / knowledge_point references a letter — validate.py warns on that.
Usage: python3 scripts/rebalance_keys.py exams/saa-c03/quiz-*.json
"""
from __future__ import annotations

import hashlib
import json
import random
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path


def target_positions(n_questions: int, n_slots: int) -> list[int]:
    """Round-robin list of target correct-positions, shuffled deterministically."""
    seq = [i % n_slots for i in range(n_questions)]
    random.Random(42).shuffle(seq)
    return seq


def rebalance(path: Path) -> None:
    data = json.loads(path.read_text())
    qs = data["questions"]
    singles = [q for q in qs if q["type"] == "single_choice"]
    multis = [q for q in qs if q["type"] == "multiple_response"]

    # Singles: assign each a target position for the correct option.
    for q, target in zip(singles, target_positions(len(singles), 4)):
        rng = random.Random(hashlib.md5(q["id"].encode()).hexdigest())
        correct = [o for o in q["options"] if o["correct"]]
        wrong = [o for o in q["options"] if not o["correct"]]
        rng.shuffle(wrong)
        new = wrong[:target] + correct + wrong[target:]
        for i, o in enumerate(new):
            o["letter"] = "ABCDE"[i]
        q["options"] = new

    # Multis: cycle through all C(5,2)=10 pairs.
    pairs = list(combinations(range(5), 2))
    order = target_positions(len(multis), len(pairs))
    for q, pi in zip(multis, order):
        rng = random.Random(hashlib.md5(q["id"].encode()).hexdigest())
        correct = [o for o in q["options"] if o["correct"]]
        wrong = [o for o in q["options"] if not o["correct"]]
        rng.shuffle(wrong); rng.shuffle(correct)
        slots = pairs[pi]
        new: list[dict] = []
        ci = wi = 0
        for pos in range(5):
            if pos in slots:
                new.append(correct[ci]); ci += 1
            else:
                new.append(wrong[wi]); wi += 1
        for i, o in enumerate(new):
            o["letter"] = "ABCDE"[i]
        q["options"] = new

    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    dist_s = Counter(next(o["letter"] for o in q["options"] if o["correct"]) for q in singles)
    dist_m = Counter("".join(o["letter"] for o in q["options"] if o["correct"]) for q in multis)
    print(f"{path.name}: single {dict(sorted(dist_s.items()))} · multi {dict(sorted(dist_m.items()))}")


if __name__ == "__main__":
    for p in sys.argv[1:]:
        rebalance(Path(p))
