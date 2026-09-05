# Exam Hub

Personal certification prep platform. One static engine (`app.html`), one JSON content pack per exam under `exams/<id>/`.

- `index.html` — hub landing page
- `app.html?exam=<id>` — engine: Cram · Rapid Recall (Leitner boxes) · Decision Tables · per-domain quizzes with a "why" on every option · timed Exam Sim · Traps · Mistakes · Flagged · cross-device progress export
- `exams/<id>/manifest.json` — exam metadata, domains, file map
- `exams/<id>/quiz-d*.json` — question banks (see `exams/saa-c03/SPEC.md` for schema)
- `exams/<id>/cheatsheets.json` — Tier-S, per-domain facts, decision tables, mnemonics, numbers
- `exams/<id>/traps-tips.json` — traps, tips, keyword→service, 80/20 focus
- `exams/<id>/rapid-recall.json` — active-recall cards (pick / flip)

Add a new exam: create the folder, write a manifest, drop in the JSON files, add a card in `index.html`.

Hosted on GitHub Pages. Progress is stored in `localStorage` per device; use the footer "Sync / export progress" to move it.
