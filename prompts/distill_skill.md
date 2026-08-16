# SKILL.md Writing Guide

SKILL.md is the entry point an agent loads. It must teach the agent to
THINK AND ACT according to the book - not to recite the book.

## Frontmatter

```yaml
---
name: <slug>          # must equal the skill directory name
description: <1-3 sentences: what the skill does + when to use it.
              Include trigger phrases an agent can match against user
              requests. Mention the source book by title.>
---
```

## Body

Use the section list required by the category's distillation profile
(base list unless overridden). The base list:

1. **Purpose** - what this skill makes the agent good at. One paragraph.
2. **Use When** - concrete trigger conditions (user situations).
3. **Do Not Use When** - explicit anti-triggers (lookalike but wrong tasks).
4. **Core Mental Model** - the one central idea of the book, stated
   operationally, with a tiny diagram-in-text if it helps.
5. **Core Principles** - the 5-10 load-bearing principles, one line each,
   referencing `references/principles.md` entries (P1, P2, ...).
6. **Operating Procedure** - the main step-by-step procedure(s) the agent
   runs when the skill triggers. Numbered, imperative, with decision points.
7. **Decision Rules** - crisp if/then rules the agent applies without
   thinking twice.
8. **Failure Modes** - how applying the book's method goes wrong, and the
   correction for each.
9. **How to Handle Uncertainty** - how the agent should express confidence,
   unknowns, and disagreement per the book's epistemics.
10. **How to Use the References** - which reference file to open for which
    need, and the provenance/content-type legend.
11. **Final Quality Check** - a short self-check list the agent runs before
    answering with this skill (e.g. "Did I separate decision quality from
    outcome quality? Did I overstate any claim?").

Category profiles may add or replace sections - follow the profile you were
given.

## Hard rules

- No chapter summaries. No "Part One discusses...".
- Reference entries by their ids (P1, F2, PR3) instead of restating them.
- The Operating Procedure must be executable by an agent on a fresh problem,
  not a description of the book's table of contents.
- Keep it under ~250 lines. Detail goes to references/.
