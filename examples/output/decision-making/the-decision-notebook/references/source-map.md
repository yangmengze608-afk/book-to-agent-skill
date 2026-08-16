# Source Map

> Every entry in this skill, mapped to its origin in "The Decision
> Notebook" (CC0 1.0, by the book-to-agent-skill authors). Source format
> is Markdown with chapter headings, so provenance uses chapter + section;
> page numbers do not exist and are never invented.

## Content-type legend

- `SOURCE FACT` - the book states this (a description of the book's method)
- `AUTHOR CLAIM` - the author's prescription or assertion
- `EVIDENCE` - evidence the author cites for a claim
- `DISTILLER INFERENCE` - operational rule derived by this skill; always
  carries `derived_from` ids instead of a source

## Entry → chapter map

| Entry | Type | Chapter | Section |
|---|---|---|---|
| P1 | AUTHOR CLAIM | 1 | Every Decision Is a Bet |
| P2 | AUTHOR CLAIM | 2 | Resulting: The Trap of Judging by Outcomes |
| P3 | AUTHOR CLAIM | 2 | Resulting: The Trap of Judging by Outcomes |
| P4 | AUTHOR CLAIM | 3 | Updating: Hearing the Crowd Correctly |
| P5 | AUTHOR CLAIM | 3 | Updating: Hearing the Crowd Correctly |
| P6 | AUTHOR CLAIM | 5 | Sizing: Bold When Right, Careful When Unsure |
| P7 | AUTHOR CLAIM | 4 | The Decision Journal |
| P8 | AUTHOR CLAIM | 6 | Premortems and Tripwires |
| P9 | EVIDENCE | 6 | Premortems and Tripwires |
| P10 | AUTHOR CLAIM | 8 | The Practicing Decider |
| P11 | DISTILLER INFERENCE | derived | (P1-P10, whole book) |
| F1 | SOURCE FACT | 1 | Every Decision Is a Bet |
| F2 | SOURCE FACT | 4 | The Decision Journal |
| F3 | SOURCE FACT | 6 | Premortems and Tripwires |
| F4 | SOURCE FACT | 6 | Premortems and Tripwires |
| F5 | SOURCE FACT | 7 | Deciding in Groups: Permission to Disagree |
| F6 | SOURCE FACT | 5 | Sizing: Bold When Right, Careful When Unsure |
| PR1 | DISTILLER INFERENCE | derived | (P1, P6, F1-F4) |
| PR2 | DISTILLER INFERENCE | derived | (P2, P3, P5, P7) |
| PR3 | SOURCE FACT | 7 | Deciding in Groups: Permission to Disagree |
| EX1-EX3 | DISTILLER INFERENCE | derived | new situations, not from the book |
| L1-L3 | SOURCE FACT | 8 | The Practicing Decider |
| L4 | DISTILLER INFERENCE | derived | (P1, P4, L1, L2) |

## Source confidence note

All SOURCE FACT / AUTHOR CLAIM / EVIDENCE entries carry
`source_confidence: high`: the source book is short, structured in eight
clearly headed chapters, and every entry above quotes its chapter and
section heading directly. DISTILLER INFERENCE entries need no source -
they carry `derived_from` instead, so the chain from the book to every
operational rule stays auditable.
