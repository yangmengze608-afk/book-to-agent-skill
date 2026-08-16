# Common Distillation Rules (apply to every category)

You are distilling an entire book into ONE Agent Skill. The output is an
operating manual that makes an agent **do things the book's way** - not a
summary of what the book says.

## The four content types (MANDATORY tagging)

Every distilled principle, framework, procedure, or claim must be tagged
with exactly one type:

- `SOURCE FACT` - things the book explicitly states (definitions, described
  steps, the author's account of events).
- `AUTHOR CLAIM` - the author's own prescriptions, opinions, or arguments
  (most "should" statements).
- `EVIDENCE` - studies, cases, data, or anecdotes the author cites in
  support of claims.
- `DISTILLER INFERENCE` - operational rules YOU derive from the book to make
  it usable by an agent. These were never stated verbatim by the author.

Never present a DISTILLER INFERENCE as the author's words. When in doubt,
tag it as DISTILLER INFERENCE.

## Provenance (MANDATORY)

Every `SOURCE FACT`, `AUTHOR CLAIM`, and `EVIDENCE` entry carries source
provenance in this exact format, inside the reference file:

```markdown
### P3. <short title>
- type: SOURCE FACT
- source: chapter 6, section "The crowd and the weather"
- source_confidence: high
<body: the distilled, operational content>
```

- Use `chapter N` plus `section "..."` or a heading. Add `pages 122-126`
  ONLY if the source format reliably carries page numbers (e.g. a PDF with
  a text layer and stable pagination). Never invent page numbers.
- `source_confidence` is high / medium / low: how sure you are the item
  comes from that location.
- `DISTILLER INFERENCE` entries carry `- derived_from: P2, F1` instead of
  `- source:` (pointers to the entries they were derived from).

## Copyright

- Paraphrase, abstract, and transform. Quote at most 25 consecutive words.
- No chapter-by-chapter summaries. No compressed reproduction of the book.
- The goal is operational distillation, not a compressed pirated copy.

## Style

- Imperative voice ("State the bet", "Separate decision from outcome").
- Each entry must be independently useful when read alone.
- Keep SKILL.md compact (roughly 150-250 lines): it is the operating manual;
  detail belongs in references/.
- Examples in examples.md are paraphrased scenarios, not book excerpts.
