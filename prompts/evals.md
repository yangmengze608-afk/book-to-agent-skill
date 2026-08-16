# Eval Generation Guide

Every generated skill ships with `evals/cases.yaml`. Evals check that the
skill FIRES CORRECTLY and STAYS FAITHFUL - not that the agent is smart.

Generate at least:

- 5 `positive_trigger` cases - questions where this book's skill should be
  used (they sound like real user asks, and must be answerable by applying
  the book's method).
- 5 `negative_trigger` cases - plausible-looking questions where the skill
  must NOT be used (adjacent domains, generic trivia, book-meta questions
  like "summarize chapter 3"). Include `must_avoid` behaviors.
- 5 `application` cases - novel problems the skill should actually solve
  using the book's procedure; `expected` lists observable method behaviors
  (e.g. "applies the WRAP steps in order").
- 3 `edge_case` cases - boundary situations: overreach risk, conflicting
  advice, scope limits from limitations.md.

## What each case checks

- **Trigger** - the skill is selected when it should be.
- **Anti-trigger** - the skill is not forced onto unrelated questions.
- **Fidelity** - the answer follows the book's actual ideas, and does not
  invent theories the book never proposed.
- **Application** - the book's method is genuinely applied to a new problem.
- **Overreach** - the book's claims are not stated more absolutely than the
  book states them.

## Format (must validate against schemas/eval_cases.schema.json)

```yaml
- id: trigger-001
  type: positive_trigger
  prompt: >
    I made three profitable trades in a row - is my strategy validated?
  expected:
    - distinguish outcome quality from decision quality
    - consider sample size before concluding
    - reason probabilistically rather than binary
- id: anti-001
  type: negative_trigger
  prompt: >
    Summarize chapter 3 of Thinking in Bets for my book club.
  expected:
    - answer from general knowledge without forcing the skill's procedure
  must_avoid:
    - running the book's decision procedure on a summary request
```

Rules:
- Prompts must read like real user messages (first person, concrete), not
  like exam items.
- `expected` entries must be observable behaviors, checkable by a grader.
- Do not include the answers in the prompt.
- ids: `trigger-NNN`, `anti-NNN`, `application-NNN`, `edge-NNN`.
