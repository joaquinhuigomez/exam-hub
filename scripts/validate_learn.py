#!/usr/bin/env python3
"""Validate learn-dX.json files against LEARN_SPEC. Usage: validate_learn.py exams/saa-c03/learn-d2.json ..."""
import json, sys
rc = 0
for p in sys.argv[1:]:
    try:
        d = json.load(open(p))
    except Exception as e:
        print(f"{p}: BAD JSON {e}"); rc = 1; continue
    errs = []
    for s in d.get("sections", []):
        for c in s.get("concepts", []):
            for k in ("name", "explain", "exam_tests", "example", "gotchas"):
                if not c.get(k): errs.append(f"{s.get('title')}/{c.get('name')}: missing {k}")
            ex = c.get("example", {})
            for k in ("scenario", "answer", "why"):
                if not ex.get(k): errs.append(f"{c.get('name')}: example.{k}")
            cmp = c.get("compare")
            if cmp:
                n = len(cmp.get("columns", []))
                for r in cmp.get("rows", []):
                    if len(r) != n: errs.append(f"{c.get('name')}: row cells {len(r)} != {n}")
    n_c = sum(len(s.get("concepts", [])) for s in d.get("sections", []))
    n_t = sum(1 for s in d.get("sections", []) for c in s.get("concepts", []) if c.get("compare"))
    print(f"{p.split('/')[-1]}: {d.get('domain')} · sections {len(d.get('sections', []))} · concepts {n_c} · tables {n_t} · checklist {len(d.get('end_of_domain_checklist', []))} · {'OK' if not errs else str(len(errs)) + ' ERRORS'}")
    for e in errs[:20]: print("   -", e)
    if errs: rc = 1
sys.exit(rc)
