<div align="center">

# Ykmmz Agent Skills

**A growing collection of reusable Agent Skills built for real workflows — not prompt snippets.**

[简体中文](./README.md) · **English**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](./LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent-Skills-black)](./skills/README.md)

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

## Repository structure

```text
.
├── README.md
├── README_EN.md
├── SKILL.md                     # current root entry: Book → Agent Skill (kept for compatibility)
├── skills/
│   ├── README.md                # multi-skill index
│   ├── book-to-agent/
│   │   ├── README.md
│   │   └── SKILL.md
│   └── image-style-clone/
│       ├── README.md
│       ├── SKILL.md
│       ├── references/
│       ├── schemas/
│       ├── examples/
│       └── evals/
└── ...                          # remaining Book → Agent supporting assets at the root
```

You can also start from [`skills/README.md`](./skills/README.md), which acts as the multi-skill index.

## Skills

| Skill | Path | What it does | Status |
|---|---|---|---|
| **Book → Agent Skill** | [`skills/book-to-agent/`](./skills/book-to-agent/README.md) | Turns one book into one reusable Agent Skill using classification-specific distillation, provenance, and evals. | ✅ Available |
| **Image Style Clone** | [`skills/image-style-clone/`](./skills/image-style-clone/README.md) | Cleans reference images, extracts per-image JSON evidence, distills shared Style DNA, merges a new user scene, then compiles a same-style generation prompt. | ✅ Available |

> This repository started as the single-purpose `book-to-agent-skill` project. It is now being upgraded into a broader Agent Skill collection. The migration strategy is **unify the entry points first, migrate internals gradually** — so each skill gets a stable home under `skills/` without breaking existing workflows.

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

Main entry: [`skills/book-to-agent/README.md`](./skills/book-to-agent/README.md)

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

## Installation

```bash
git clone https://github.com/yangmengze608-afk/book-to-agent-skill.git
cd book-to-agent-skill
python -m venv venv && source venv/bin/activate
pip install -e ".[dev]"
```

> The repository has just been renamed. GitHub will redirect the former URL. The install command will be updated to the final canonical repository path once the connector refreshes.

## Usage

```bash
book2skill init ./book.epub --workspace ./ws
book2skill distill --workspace ./ws
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

## Principles

1. **Capability over summary** — produce an operating method, not a compressed book report.
2. **Evidence over vibes** — preserve provenance for claims that matter.
3. **Honest uncertainty** — use confidence and alternatives instead of fake certainty.
4. **Progressive disclosure** — keep `SKILL.md` executable; move depth into `references/`.
5. **Evaluation by default** — a skill is not finished just because the Markdown looks good.
6. **One clear job per skill** — keep triggering and boundaries legible.

## Roadmap

- [x] Book → Agent Skill
- [x] Image Style Clone
- [x] Unified `skills/` index entry points
- [ ] Continue migrating Book → Agent supporting assets into `skills/book-to-agent/`
- [ ] Add dedicated English READMEs for individual skills
- [ ] Shared skill index and installation conventions
- [ ] Cross-skill routing
- [ ] More reusable Chinese-first Agent Skills

## License

MIT. See [LICENSE](./LICENSE).

For book-derived outputs, do not commit copyrighted source texts into the repository. Distillates should be transformative, paraphrased, and provenance-aware.
