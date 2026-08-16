# book-to-agent-skill

> **Turn a book into one reusable Agent Skill — classify first, distill second.**
>
> **One book → one skill by default.** Never a pile of chapter summaries, never a RAG bot.

Give it a book (`.pdf` / `.epub` / `.txt` / `.md`). It classifies the book into a capability category, picks a **category-specific distillation strategy**, and produces **one Agent Skill** — a `SKILL.md` operating manual plus `references/` and an auto-generated eval suite — with source provenance for every load-bearing claim.

```text
Thinking in Bets
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

**Is:** a meta-skill + CLI pipeline: `Book → Classification → Distillation → ONE Agent Skill → Eval`.

**Is not:** a PDF summarizer, chat-with-PDF, RAG chatbot, knowledge-graph platform, multi-user SaaS, or a "one chapter → one skill" splitter.

---

## Architecture

```text
Book (.pdf/.epub/.txt/.md)
 ↓ 1. Ingest            extract text; detect scanned PDFs → "OCR required"
 ↓ 2. Structure         detect chapters (md headings / chapter patterns / synthetic chunks)
 ↓ 3. Classify          ONE primary category + subcategory + confidence + alternatives
 ↓ 4. Select strategy   category → taxonomy/distillation_profiles/<category>.yaml
 ↓ 5. Distill           whole book → SKILL.md + references/ (4 content types, provenance)
 ↓ 6. Eval              auto-generate ≥18 cases (trigger/anti-trigger/application/edge)
 ↓ 7. QA                validator: schemas, required sections, provenance, eval counts
 ↓ 8. Output            output/<category>/<slug>/
```

**Division of labor:** the CLI does deterministic work (extraction, structure detection, scaffolding, schema validation, installation). **The calling agent does the judgment work** (classification, distillation, eval authoring) following the binding prompts in `prompts/`. Optional LLM providers exist (`src/.../providers/`) but no API key is required to use this project — the default provider delegates reasoning to the agent running the skill.

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
# 1. Ingest + structure + heuristic pre-classification
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

## Output format

```text
output/<primary_category>/<slug>/
├── SKILL.md          # operating manual, not a book report (≤ ~250 lines)
├── BOOK.yaml         # title/author/category/tags/confidence/language/generated_at…
├── references/       # progressive disclosure — read on demand
└── evals/cases.yaml
```

`SKILL.md` frontmatter follows the Agent Skills format (`name` + `description` with use-when triggers) so the skill drops straight into Claude Code / Codex-style skill directories.

## Eval

Every generated skill must ship `evals/cases.yaml` with minimums — **5 positive trigger, 5 negative trigger, 5 application, 3 edge case** — validated against [schemas/eval_cases.schema.json](schemas/eval_cases.schema.json):

- **Trigger** — the skill fires when the book's method applies
- **Anti-trigger** — irrelevant questions don't invoke it (`must_avoid` required)
- **Application** — the method actually solves a new problem
- **Fidelity / Overreach** — edge cases probe for invented theory and over-absolute claims

```yaml
- id: trigger-001
  type: positive_trigger
  prompt: >
    我连续三次投资都赚钱了，是不是说明我的判断方法已经得到验证？
  expected:
    - distinguish outcome quality from decision quality (no resulting)
    - point out the small sample size and what it can/cannot prove
    - reason probabilistically instead of issuing a verdict
  must_avoid:
    - concluding "you are validated" or "you are just lucky"
```

## Taxonomy

One flat, extensible level of 16 categories in [taxonomy/categories.yaml](taxonomy/categories.yaml) (keywords + subcategories), each with a distillation profile in [taxonomy/distillation_profiles/](taxonomy/distillation_profiles/):

`decision-making` · `investing-finance` · `business-strategy` · `psychology-behavior` · `research-science` · `learning-education` · `writing` · `communication-negotiation` · `productivity` · `leadership-management` · `technology-engineering` · `creativity-design` · `philosophy-thinking` · `health-performance` · `reference-knowledge` · `other`

Adding a category = add one entry to `categories.yaml` + one profile YAML. Profiles merge over [\_base.yaml](taxonomy/distillation_profiles/_base.yaml).

## Limitations

- **No OCR.** Scanned PDFs are detected and reported as `OCR required`; an extension point exists but V1 does not transcribe.
- **Provenance granularity** is chapter/section/heading — page numbers are used only when the source format reliably provides them, never invented.
- **Distillation quality depends on the reading agent.** The CLI enforces structure, schemas, provenance, and eval counts; it cannot fully machine-check intellectual fidelity.
- **English/Chinese tested**; other languages work best with clean structure markers.
- **One skill per book, by design** — multi-book fusion is explicitly out of scope for V1.

## Prior Art

- **[virgiliojr94/book-to-skill](https://github.com/virgiliojr94/book-to-skill)** and **[apple-ouyang/book-to-skill](https://github.com/apple-ouyang/book-to-skill)** — early explorations of turning book content into skills. What they get right: skill-format output, chapter-aware processing. Where this project differs: classification-driven distillation strategies (no single generic summarization prompt), hard four-type content labeling with provenance, and a built-in eval contract.
- **OpenAI/Anthropic Agent Skills format** (`SKILL.md` + `references/` with progressive disclosure) — this project targets that format as its output and follows its conventions; no code copied.
- Generic "chat with your PDF" / RAG tooling — different problem: retrieval answers questions about a book; this project produces a *reusable operating capability* distilled from it.

No source code was copied from any third-party project; all code here is original (MIT).

## Roadmap

```text
V2: multi-book library
V3: cross-book deduplication
V4: book skill routing (which book-skill to invoke when several apply)
V5: GUI/plugin
```

Deliberately **not** in V1: web UI, SaaS, accounts, vector DB, knowledge graph, multi-agent orchestration, auto-download of books, auto-splitting a book into many skills.

## License

[MIT](LICENSE). The example book *The Decision Notebook* is dedicated to the public domain (CC0). Do not commit copyrighted book texts into this repository — distillates are paraphrased transformations with citations, not compressed copies.
