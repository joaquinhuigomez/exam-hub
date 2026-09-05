#!/usr/bin/env python3
"""Validate an exam content pack against the engine's expectations.

Usage: python3 scripts/validate.py exams/saa-c03
Exits non-zero on any structural error. Warnings are printed but do not fail.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

REQUIRED_Q = {"id", "type", "difficulty", "scenario", "stem", "options", "knowledge_point", "trap_alert"}
VALID_TYPES = {"single_choice", "multiple_response"}
VALID_DIFF = {"easy", "medium", "hard"}


def load(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        print(f"  MISSING  {path.name}")
        return None
    except json.JSONDecodeError as exc:
        print(f"  BAD JSON {path.name}: {exc}")
        return None


def check_questions(path: Path, domain_id: str) -> tuple[int, list[str]]:
    errors: list[str] = []
    data = load(path)
    if data is None:
        return 0, [f"{path.name}: unreadable"]
    qs = data.get("questions", [])
    ids = Counter(q.get("id") for q in qs)
    for dup, n in ids.items():
        if n > 1:
            errors.append(f"{path.name}: duplicate id {dup} ×{n}")
    diff = Counter()
    types = Counter()
    for q in qs:
        qid = q.get("id", "?")
        missing = REQUIRED_Q - set(q)
        if missing:
            errors.append(f"{qid}: missing {sorted(missing)}")
        if q.get("type") not in VALID_TYPES:
            errors.append(f"{qid}: bad type {q.get('type')}")
        if q.get("difficulty") not in VALID_DIFF:
            errors.append(f"{qid}: bad difficulty {q.get('difficulty')}")
        if not str(qid).startswith(domain_id + "-"):
            errors.append(f"{qid}: id does not start with {domain_id}-")
        opts = q.get("options", [])
        letters = [o.get("letter") for o in opts]
        correct = [o for o in opts if o.get("correct") is True]
        if q.get("type") == "single_choice" and (len(opts) != 4 or len(correct) != 1):
            errors.append(f"{qid}: single_choice needs 4 options / 1 correct (got {len(opts)}/{len(correct)})")
        if q.get("type") == "multiple_response" and (len(opts) != 5 or len(correct) != 2):
            errors.append(f"{qid}: multiple_response needs 5 options / 2 correct (got {len(opts)}/{len(correct)})")
        if letters != [chr(65 + i) for i in range(len(opts))]:
            errors.append(f"{qid}: letters not sequential A.. ({letters})")
        for o in opts:
            if not o.get("why") or len(o.get("why", "")) < 20:
                errors.append(f"{qid}{o.get('letter')}: why too short")
            if not o.get("text"):
                errors.append(f"{qid}{o.get('letter')}: empty text")
        diff[q.get("difficulty")] += 1
        types[q.get("type")] += 1
    singles = [q for q in qs if q.get("type") == "single_choice"]
    key_dist = Counter(next((o["letter"] for o in q.get("options", []) if o.get("correct")), "?") for q in singles)
    if singles and max(key_dist.values()) > 0.45 * len(singles):
        errors.append(f"{path.name}: answer-key position bias {dict(key_dist)} — run scripts/rebalance_keys.py")
    multis = [q for q in qs if q.get("type") == "multiple_response"]
    pair_dist = Counter("".join(o["letter"] for o in q.get("options", []) if o.get("correct")) for q in multis)
    if len(multis) >= 4 and max(pair_dist.values()) > 0.5 * len(multis):
        errors.append(f"{path.name}: multi-response pair bias {dict(pair_dist)} — run scripts/rebalance_keys.py")
    for q in qs:
        blob = " ".join(o.get("why", "") for o in q.get("options", [])) + q.get("knowledge_point", "") + q.get("trap_alert", "")
        if re.search(r"\b[Oo]ption [A-E]\b", blob):
            print(f"  WARN {q.get('id')}: text references an option letter — rebalancing would break it")
    print(f"  {path.name}: {len(qs)} Q · {dict(diff)} · {dict(types)} · keys {dict(sorted(key_dist.items()))}")
    return len(qs), errors


def main(pack: Path) -> int:
    manifest = load(pack / "manifest.json")
    if manifest is None:
        return 1
    print(f"{manifest['exam']['code']} — {manifest['exam']['name']}")
    errors: list[str] = []
    total = 0
    for d in manifest["domains"]:
        n, errs = check_questions(pack / d["questions_file"], d["id"])
        total += n
        errors += errs
    files = manifest.get("files", {})
    cs = load(pack / files["cheatsheets"]) if files.get("cheatsheets") else None
    if cs:
        print(f"  cheatsheets: tier_s={len(cs.get('tier_s_must_memorize_cold', []))} "
              f"domains={ {k: len(v) for k, v in cs.get('domains', {}).items()} } "
              f"tables={len(cs.get('decision_tables', []))} mnemonics={len(cs.get('mnemonics', []))} "
              f"numbers={len(cs.get('numbers_to_memorize', []))}")
        for t in cs.get("decision_tables", []):
            ncol = len(t.get("columns", []))
            for r in t.get("rows", []):
                if len(r) != ncol:
                    errors.append(f"table {t.get('id')}: row has {len(r)} cells, expected {ncol}")
    tr = load(pack / files["traps"]) if files.get("traps") else None
    if tr:
        print(f"  traps: traps={len(tr.get('traps', []))} tips={len(tr.get('tips', []))} "
              f"keyword_pairs={len(tr.get('keyword_to_service', []))} focus={len(tr.get('top_focus_8020', []))}")
    rr = load(pack / files["rapid_recall"]) if files.get("rapid_recall") else None
    if rr:
        cards = rr.get("cards", [])
        kinds = Counter(c.get("kind") for c in cards)
        doms = Counter(c.get("domain") for c in cards)
        print(f"  recall: {len(cards)} cards · {dict(kinds)} · {dict(doms)}")
        for c in cards:
            if len(c.get("distractors", [])) != 3:
                errors.append(f"{c.get('id')}: needs exactly 3 distractors")
            if c.get("answer") in c.get("distractors", []):
                errors.append(f"{c.get('id')}: answer appears in distractors")
            if not c.get("why"):
                errors.append(f"{c.get('id')}: missing why")
    print(f"  TOTAL questions: {total}")
    if errors:
        print(f"\n{len(errors)} ERROR(S):")
        for e in errors[:60]:
            print("  -", e)
        return 1
    print("  OK — no structural errors")
    return 0


if __name__ == "__main__":
    sys.exit(main(Path(sys.argv[1] if len(sys.argv) > 1 else "exams/saa-c03")))
