# Learning Guide Spec (learn-dX.json)

Purpose: a PURE LEARNING page (not drills). Joaquin reads this top-to-bottom to build the mental models, then drills. He is intelligent, ADHD, ~50% conversant with AWS already (holds Cloud Practitioner + GenAI Developer Pro). He learns from: a crisp mental model, then HOW THE EXAM PHRASES IT, then a worked example, then a contrast table, then the gotchas. Not passive prose. Every paragraph must carry a decision rule or a fact that gets tested.

Voice: senior AWS SA explaining to a smart peer over coffee. Short sentences. Concrete. No marketing fluff, no "AWS offers a wide range of…". Numbers where they are tested.

## Schema (write EXACTLY; validate with python3 -m json.tool)
```json
{
  "domain": "D1",
  "title": "Design Secure Architectures",
  "weight": 0.30,
  "intro": "3–5 sentences: what this domain REALLY tests, the 3 mental models that unlock it, and how many questions to expect (~20 of 65).",
  "sections": [
    {
      "id": "iam-model",
      "title": "The IAM evaluation model",
      "summary": "One sentence: the rule that this section teaches.",
      "concepts": [
        {
          "name": "SCP vs IAM policy vs permission boundary vs resource policy",
          "explain": "3–7 sentences. The mental model in plain English. Explain the WHY behind the behaviour, not just the what. Use \\n for paragraph breaks sparingly.",
          "exam_tests": "How the exam phrases this. The trigger words. What single fact discriminates the right answer.",
          "example": {
            "scenario": "2–3 sentence mini-scenario in exam voice.",
            "answer": "The correct move (one line).",
            "why": "2–3 sentences explaining the discriminating fact and why the tempting alternative fails."
          },
          "compare": {                        // OPTIONAL, include when a contrast table helps
            "columns": ["Mechanism", "Grants?", "Scope", "Use when"],
            "rows": [["SCP", "No — bounds only", "Org/OU/account", "Guardrails across accounts"], ["..."]]
          },
          "gotchas": ["3–6 bullet traps, each one line, each a testable fact"],
          "numbers": ["OPTIONAL: tested limits, e.g. 'KMS deletion window 7–30 days'"],
          "mnemonic": "OPTIONAL: only if genuine"
        }
      ]
    }
  ],
  "end_of_domain_checklist": ["10–15 one-line 'can I…' self-checks, e.g. 'I can say why a gateway endpoint is free and an interface endpoint is not'"]
}
```
- 5–7 sections per domain, 2–4 concepts per section → 14–22 concepts per domain, covering the domain's task statements MECE.
- Every concept MUST have explain, exam_tests, example, gotchas. compare on at least half of them.
- Facts must be current as of 2025–2026. If a number is uncertain and not load-bearing, omit it.
