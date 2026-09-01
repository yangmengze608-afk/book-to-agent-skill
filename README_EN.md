<div align="center">

# Ykmmz Agent Skills

**A growing collection of reusable Agent Skills built for real workflows — not prompt snippets.**

[简体中文](./README.md) · **English**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent-Skills-black)](#skills)

</div>

---

## What is this?

**Ykmmz Agent Skills** is my open-source collection of reusable Agent Skills.

The goal is not to collect isolated prompts. Each skill should turn a repeatable method into an operating capability an agent can reliably invoke, execute, validate, and reuse.

A skill in this repository should ideally contain:

- a clear `SKILL.md` operating manual;
- explicit use / do-not-use boundaries;
- deterministic schemas or scripts where useful;
- progressive-disclosure references;
- eval cases that test triggering, application, fidelity, and edge cases;
- honest uncertainty handling instead of fabricated confidence.

## Skills

| Skill | What it does | Status |
|---|---|---|
| **Book → Agent Skill** | Turns one book into one reusable Agent Skill using classification-specific distillation, provenance, and evals. | ✅ Available |
| **Image Style Clone** | Cleans reference images, extracts per-image JSON evidence, distills shared Style DNA, merges a new user scene, then compiles a same-style generation prompt. | 🧪 Integration in progress |

> The repository is being upgraded from the original `book-to-agent-skill` project into a broader Agent Skill collection. Existing paths are intentionally kept stable while the new multi-skill structure is migrated.

---

# Book → Agent Skill

> **One book → one reusable Agent Skill. Classify first, distill second.**

Give it a book (`.pdf` / `.epub` / `.txt` / `.md`). The pipeline classifies the book into a capability category, selects a category-specific distillation strategy, and produces **one Agent Skill** — a `SKILL.md` operating manual plus `references/` and an auto-generated eval suite — with provenance for load-bearing claims.

```text
Book
  ↓
Classification
  ↓
Category-specific distillation strategy
  ↓
ONE reusable Agent Skill
  ├── SKILL.md
  ├── BOOK.yaml
  ├── references/
  └── evals/cases.yaml
```

The success test is simple: the generated skill should make an agent **act according to the book's method**, not merely know what the book said.

## Why classification comes first

A decision-making book, a psychology book, and an engineering book should not be distilled with the same generic “summarize the key points” prompt.

The current taxonomy contains 16 capability categories, including:

`decision-making` · `investing-finance` · `business-strategy` · `psychology-behavior` · `research-science` · `learning-education` · `writing` · `communication-negotiation` · `productivity` · `leadership-management` · `technology-engineering` · `creativity-design` · `philosophy-thinking` · `health-performance` · `reference-knowledge` · `other`

Each category selects a dedicated profile from `taxonomy/distillation_profiles/`, defining what should be extracted, what epistemic guardrails apply, and which sections/evals are required.

## Four content types

Every reference entry is explicitly typed so inference is not passed off as source material:

- `SOURCE FACT` — the source states this;
- `AUTHOR CLAIM` — the author's prescription or assertion;
- `EVIDENCE` — evidence cited in the source;
- `DISTILLER INFERENCE` — an operational inference derived by the distiller and linked back to its basis.

## Architecture

```text
Book (.pdf/.epub/.txt/.md)
 ↓ 1. Ingest
 ↓ 2. Structure detection
 ↓ 3. Classify
 ↓ 4. Select category strategy
 ↓ 5. Distill
 ↓ 6. Generate evals
 ↓ 7. QA / schema validation
 ↓ 8. Output
```

The CLI handles deterministic work such as extraction, structure detection, scaffolding, validation, and installation. The calling agent handles judgment-heavy work such as classification, distillation, and eval authoring.

## Installation

```bash
git clone https://github.com/yangmengze608-afk/book-to-agent-skill.git
cd book-to-agent-skill
python -m venv venv && source venv/bin/activate
pip install -e ".[dev]"
```

> GitHub redirects the former repository URL after a rename. The install commands will be updated to the final repository name once the connector has refreshed the new canonical path.

Requires Python ≥ 3.9. Main dependencies: `pypdf`, `PyYAML`, `jsonschema`.

## Usage

```bash
book2skill init ./book.epub --workspace ./ws
# agent writes classification.yaml
book2skill distill --workspace ./ws
# agent fills SKILL.md / references / evals
book2skill finalize --workspace ./ws
```

Convenience commands:

```bash
book2skill run ./book.epub --workspace ./ws
book2skill doctor
```

## Eval contract

Every generated book skill ships with at least 18 eval cases:

- 5 positive trigger cases;
- 5 negative trigger cases;
- 5 application cases;
- 3 edge / fidelity cases.

The validator checks structure and minimum contracts, while the evals probe whether the generated skill actually applies the source method without overreaching.

## Principles

1. **Capability over summary** — produce an operating method, not a compressed book report.
2. **Evidence over vibes** — preserve provenance for claims that matter.
3. **Honest uncertainty** — use confidence and alternatives instead of fake certainty.
4. **Progressive disclosure** — keep `SKILL.md` executable; move depth into `references/`.
5. **Evaluation by default** — a skill is not finished just because the Markdown looks good.
6. **One clear job per skill** — keep triggering and boundaries legible.

## Roadmap

- [x] Book → Agent Skill
- [x] Image Style Clone prototype
- [ ] Migrate to a clean `skills/<skill-name>/` multi-skill layout
- [ ] Shared skill index and installation conventions
- [ ] Cross-skill routing
- [ ] More reusable Chinese-first Agent Skills

## License

MIT. See [LICENSE](./LICENSE).

For book-derived outputs, do not commit copyrighted source texts into the repository. Distillates should be transformative, paraphrased, and provenance-aware.
