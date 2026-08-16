---
name: book-to-agent-skill
description: Turn a book (PDF/EPUB/TXT/MD) into ONE reusable Agent Skill - classify the book first, distill with a category-specific strategy second, with source provenance, four content-type tags, and an auto-generated eval suite. Use when the user asks to convert a book into an agent skill / claude skill / codex skill, distill a book's methods into a skill, or create a skill from a book.
---

# book-to-agent-skill (Meta Skill)

You are the reasoning engine of this pipeline. The CLI
(`book2skill` / `python -m book_to_agent_skill`) does the deterministic work:
extraction, structure detection, scaffolding, validation, installation.
YOU do the judgment work: classification, distillation, eval authoring.

**One book -> one skill. Never split a book into multiple skills.**

## Purpose

Produce an Agent Skill that makes agents *act* according to a book's method -
not a summary that tells them what the book said.

## Use When

- The user asks to turn a book into an agent skill ("make a skill from this PDF")
- The user wants a book's methodology available to their agent on demand

## Do Not Use When

- The user just wants a summary, a chat-with-PDF, or a RAG index
- The input is not a single book (articles, video, multi-book fusion -> out of scope)
- The file is a scanned PDF (no text layer) - report "OCR required" and stop

## Operating Procedure

Work in the repo checkout (this skill needs `taxonomy/`, `prompts/`,
`schemas/` from the repo; install with `pip install -e .`).

### Phase 1 - Init (deterministic)

```bash
book2skill init ./book.epub --workspace ./ws
```

Read the printed structure (chapters, words) and the heuristic
pre-classification. If ingestion reports `OCR required`, stop and tell the user.

### Phase 2 - Classification (you)

1. Read `ws/book/text.md` (or the digest embedded in
   `ws/workorder/01-classification.md`).
2. Decide ONE primary category from `taxonomy/categories.yaml`
   (16 categories; read the category descriptions if unsure).
3. Judge honestly. Confidence >= 0.9 only if the book announces itself
   unmistakably; < 0.5 means genuinely torn - say so.
4. Write `ws/classification.yaml` per `schemas/classification.schema.json`,
   with `method: agent` and a rationale grounded in the book's content.
5. Validate + scaffold:

```bash
book2skill distill --workspace ./ws
```

The chosen category's profile in `taxonomy/distillation_profiles/` now
defines what you must extract.

### Phase 3 - Distillation (you)

1. Read `prompts/distill_common.md` and `prompts/distill_skill.md` in full.
   They are binding: four content types, provenance format, copyright limits.
2. Read the whole book (`ws/book/text.md`). Do not distill from the digest alone.
3. Fill `ws/skill/SKILL.md` (operating manual, sections per the profile)
   and every file in `ws/skill/references/` following the profile's focus list.

Hard rules:
- Tag every entry SOURCE FACT / AUTHOR CLAIM / EVIDENCE / DISTILLER INFERENCE.
- Attach `- source: chapter N, section "..."` + `- source_confidence:` to
  sourced entries; never invent page numbers.
- Paraphrase; at most 25 consecutive words verbatim; no chapter summaries.
- SKILL.md teaches doing (procedures, decision rules), references/ hold the
  depth. Keep SKILL.md under ~250 lines.

### Phase 4 - Evals (you)

Write `ws/skill/evals/cases.yaml` per `prompts/evals.md`:
5 positive triggers, 5 negative triggers (with must_avoid), 5 applications,
3 edge cases. Prompts must sound like real user messages.

### Phase 5 - Validate + Finalize (deterministic gate)

```bash
book2skill finalize --workspace ./ws
```

If validation fails, fix the reported items and re-run. On success the skill
is installed to `output/<category>/<slug>/`.

### Phase 6 - Report to the user

Report: the classification + confidence + one-line rationale, the output path,
the eval count, validation status, and where the provenance lives.

## Decision Rules

- Ambiguous genre? Classify by the dominant teachable capability, not subject matter.
- Book fits two categories? Primary = the one with a distillation profile that
  matches the book's *method*; list the other in alternative_categories.
- Unsure between two categories after reading? Pick the better fit, set
  confidence honestly (< 0.6), and say why in the rationale.
- Book too short or not method-like (< ~8k words of substance)? Tell the user
  a skill may not add value; proceed only if they confirm.
- Never distill copyrighted content you did not ingest from the user's file.

## Failure Modes

- Chapter-summary drift -> the validator rejects it (sections check) and you
  should rewrite as procedures.
- Inflation (inventing frameworks the author never proposed) -> keep
  DISTILLER INFERENCE honest and derived_from-linked.
- Overreach (absolute claims from hedged books) -> check limitations.md covers
  contested claims; evals edge cases must probe this.
- Splitting into multiple skills -> never; one book = one skill.

## How to Handle Uncertainty

- Classification: honest confidence + alternatives, never fake certainty.
- Provenance: `source_confidence: low` when you cannot pin the location;
  never fabricate chapters either - fall back to `section "..."` from the
  structure map.

## How to Use the References

- `taxonomy/categories.yaml` - the 16 categories + keywords (classification)
- `taxonomy/distillation_profiles/*.yaml` - what to extract per category
- `prompts/*.md` - binding rules for classification, distillation, evals
- `schemas/*.json` - machine-checked contracts for classification, BOOK.yaml, evals
- `examples/output/` - one complete generated skill (The Decision Notebook)

## Final Quality Check

Before finalize, verify:
1. One skill, one category, honest confidence.
2. SKILL.md would let a fresh agent *run the book's method* on a new problem.
3. Every reference entry has a valid type + provenance/derivation link.
4. 18+ eval cases covering trigger / anti-trigger / application / edge.
5. No verbatim runs > 25 words; no chapter summaries anywhere.
