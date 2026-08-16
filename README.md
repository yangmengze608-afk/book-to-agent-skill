# book-to-agent-skill

> **Turn a book into one reusable Agent Skill — classify first, distill second.**
>
> **One book → one skill by default.** Never a pile of chapter summaries, never a RAG bot.

Give it a book (`.pdf` / `.epub` / `.txt` / `.md`). It first applies a conservative **book-only scope gate** (obvious journal articles are rejected rather than silently treated as books), then classifies the book into a capability category, picks a **category-specific distillation strategy**, and produces **one Agent Skill** — a `SKILL.md` operating manual plus `references/` and an auto-generated eval-case suite — with source provenance for every load-bearing claim.

```text
Thinking in Bets
        ↓
Scope Gate                 book / uncertain non-book → continue
        ↓
Book Classification        decision-making → uncertainty (confidence 0.94)
        ↓
Distillation Strategy      decision principles, frameworks, uncertainty handling, biases…
        ↓
output/decision-making/thinking-in-bets/
├── SKILL.md               ← teaches an agent to DECIDE the way the book teaches
├── BOOK.yaml
├── references/            ← progressive disclosure: depth lives here
└── evals/cases.yaml       ← 18 cases: trigger / anti-trigger / application / edge
```

The success test: a generated skill must make an agent **act according to the book's method** — not merely *know what the book said*.

---

## Why classification comes first

A decision-making book, a psychology book, and an engineering book should **not** be distilled with the same "summarize the key points" prompt. Each category yields a different kind of capability:

| Category | The skill extracts |
|---|---|
| `decision-making` | decision principles, frameworks, uncertainty handling, biases, procedures, failure modes |
| `investing-finance` | investment philosophy, thesis construction, risk framework, position rules, warning signs |
| `psychology-behavior` | mechanisms, constructs, causal explanations, evidence quality, interventions, misconceptions |
| `research-science` | methodology, experimental design, validity threats, statistical reasoning, reproducibility |
| `technology-engineering` | architecture, design principles, implementation patterns, debugging procedures, anti-patterns |
| `writing` | principles, workflow, editing rules, before/after patterns, checklists |
| … 16 categories total | see [Taxonomy](#taxonomy) |

Classification is stored with an **honest confidence score** and alternatives — if the book is genuinely torn between two categories, the skill says so instead of pretending certainty. The chosen category then selects a [distillation profile](taxonomy/distillation_profiles/) that defines:

- what to extract (focus areas),
- epistemic guardrails (e.g. psychology: never state a theory as absolute fact; separate author opinion from cited evidence),
- required sections for `SKILL.md`,
- example trigger / anti-trigger questions for evals.

## What this is / is not

**Is:** a meta-skill + CLI pipeline: `Book → Scope Gate → Classification → Distillation → ONE Agent Skill → Eval Cases`.

**Is not:** a PDF summarizer, chat-with-PDF, RAG chatbot, knowledge-graph platform, multi-user SaaS, or a "one chapter → one skill" splitter.

V1 is intentionally **book-only**. A PDF extension does not imply a book: obvious scholarly articles are detected from multiple independent signals (for example DOI/article labels plus formal Abstract/Methods/Results/Discussion structure) and rejected before classification. Ambiguous documents are not auto-rejected; the agent still makes the final scope judgment.

---

## Architecture

```text
Book (.pdf/.epub/.txt/.md)
 ↓ 1. Ingest            extract text; detect scanned PDFs → "OCR required"
 ↓ 2. Scope gate        conservatively reject obvious research articles
 ↓ 3. Structure         detect chapters (md headings / chapter patterns / synthetic chunks)
 ↓ 4. Classify          ONE primary category + subcategory + confidence + alternatives
 ↓ 5. Select strategy   category → taxonomy/distillation_profiles/<category>.yaml
 ↓ 6. Distill           whole book → SKILL.md + references/ (4 content types, provenance)
 ↓ 7. Eval cases        auto-generate ≥18 cases (trigger/anti-trigger/application/edge)
 ↓ 8. QA                validator: schemas, required sections, provenance, eval counts
 ↓ 9. Output            output/<category>/<slug>/
```

**Division of labor:** the CLI does deterministic work (extraction, scope checking, structure detection, scaffolding, schema validation, installation). **The calling agent does the judgment work** (classification, distillation, eval authoring) following the binding prompts in `prompts/`. Optional LLM providers exist (`src/.../providers/`) but no API key is required to use this project — the default provider delegates reasoning to the agent running the skill.

### Four content types (hard requirement)

Every reference entry is tagged, so inferences are never passed off as the author's words:

- `SOURCE FACT` — the book states this (description of the method)
- `AUTHOR CLAIM` — the author's prescription or assertion
- `EVIDENCE` — evidence the author cites
- `DISTILLER INFERENCE` — operational rule derived by the distiller; must carry `derived_from` links, never a fabricated source

### Source provenance

```yaml
- type: AUTHOR CLAIM
  source: chapter 6, section "Premortems and Tripwires"
  source_confidence: high
```

Chapter/section/heading-based (no fabricated page numbers). `source_confidence: high | medium | low` when the location can't be pinned precisely.

---

## Example

A complete, copyright-safe example ships in the repo: [examples/books/the-decision-notebook.md](examples/books/the-decision-notebook.md) — an original CC0 mini-book on decision-making — and its fully generated skill in [examples/output/decision-making/the-decision-notebook/](examples/output/decision-making/the-decision-notebook/):

```text
examples/output/decision-making/the-decision-notebook/
├── SKILL.md               operating manual: Purpose / Use When / Core Mental Model /
│                          Operating Procedure / Decision Rules / Failure Modes …
├── BOOK.yaml              metadata: category, tags, confidence, provenance stats
├── references/
│   ├── principles.md      P1–P11, each typed + sourced
│   ├── frameworks.md      named frameworks w/ inputs, steps, outputs
│   ├── procedures.md      executable step-by-step procedures
│   ├── examples.md        worked applications to new situations
│   ├── limitations.md     where the method breaks
│   └── source-map.md      entry → chapter map + content-type legend
└── evals/cases.yaml       18 cases
```

*(Conceptual examples like "Thinking in Bets" appear in docs for illustration only; no copyrighted book text is included in this repository.)*

## Installation

```bash
git clone https://github.com/yangmengze608-afk/book-to-agent-skill.git
cd book-to-agent-skill
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

Requires Python ≥ 3.9. Dependencies: `pypdf`, `PyYAML`, `jsonschema` — no LLM API key required.

## Usage

The repo root is itself a skill (`SKILL.md`) — point an agent at it and say *"turn this book into an agent skill"*. Or drive the pipeline manually:

```bash
# 1. Ingest + scope check + structure + heuristic pre-classification
book2skill init ./books/thinking-in-bets.epub --workspace ./ws

# 2. (agent) Read ws/book/text.md, write ws/classification.yaml
#    → then validate + scaffold the skill dir with the category's profile
book2skill distill --workspace ./ws

# 3. (agent) Fill ws/skill/SKILL.md, references/, evals/cases.yaml
#    per prompts/ and the selected distillation profile

# 4. Validate + install to output/
book2skill finalize --workspace ./ws
```

One-shot convenience (stops where agent reasoning is needed):

```bash
book2skill run ./book.epub --workspace ./ws
book2skill doctor        # check environment/taxonomy/schemas
```

Typical output:

```text
Classification:
  Decision Making -> uncertainty (confidence 0.94, method agent)
  alternative: psychology-behavior (0.63)
Generating skill...
Output: output/decision-making/thinking-in-bets/
Eval: 18/18 cases generated, validation passed
```

For an obvious research article, V1 stops before classification instead of pretending it is a book:

```text
error: out of scope: input appears to be a research-article (...).
book-to-agent-skill V1 is intentionally book-only.
```

## Output format

```text
output/<primary_category>/<slug>/
├── SKILL.md          # operating manual, not a book report (≤ ~250 lines)
├── BOOK.yaml         # title/author/category/tags/confidence/language/generated_at…
├── references/       # progressive disclosure — read on demand
└── evals/cases.yaml
```

## Eval

V1 generates and validates an **eval-case suite**; it does not yet execute those cases against a model and judge the responses. That runtime benchmark layer is planned separately.

Each generated skill must include at least:

- 5 positive trigger cases
- 5 negative trigger / anti-trigger cases
- 5 application cases
- 3 edge cases

The validator checks schema, counts, unique ids, and `must_avoid` behaviors on negative-trigger cases.

## Taxonomy

V1 uses one required primary category plus optional subcategory and tags. The category selects the distillation profile; tags do not change the output contract.

See `taxonomy/categories.yaml` and `taxonomy/distillation_profiles/` for the machine-readable definitions.

## Limitations

- one book at a time; articles and multi-book fusion are out of scope
- scanned/image-only PDFs require OCR before V1 can ingest them
- the research-article scope detector is intentionally high-precision rather than exhaustive; ambiguous non-book documents may still require agent judgment
- runtime eval execution/judging is not implemented yet
- classification heuristics are hints only and are capped at low confidence
- provider-backed one-shot generation depends on the configured model/provider quality
- this is alpha software; generated skills should be reviewed before important use

## Prior Art

This project was informed by public book-to-skill experiments including `virgiliojr94/book-to-skill` and `apple-ouyang/book-to-skill`. The distinguishing V1 choices here are: classification before distillation, one whole-book skill by default, category-specific distillation profiles, explicit provenance/content types, and a deterministic validation gate.

## Roadmap

- **V1.1**: real-book benchmark set + metadata and validator hardening
- **V1.2**: execute eval cases against generated skills and score behavior
- **V2**: multi-book library
- **V3**: cross-book deduplication
- **V4**: book-skill routing
- **V5**: GUI/plugin
