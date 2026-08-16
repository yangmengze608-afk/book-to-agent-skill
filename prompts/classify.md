# Book Classification Prompt

You are classifying a whole book so the right distillation strategy can be
selected. Classification determines everything downstream: what gets
extracted, which SKILL.md sections are required, and which eval cases make
sense. Take it seriously, and be honest about uncertainty.

## Input

You will receive:
- the book's title / author (if detected)
- the detected structure (chapter titles)
- a content digest (excerpts from across the book)

## Categories

The allowed primary categories are exactly those in `taxonomy/categories.yaml`:

decision-making, investing-finance, business-strategy, psychology-behavior,
research-science, learning-education, writing, communication-negotiation,
productivity, leadership-management, technology-engineering, creativity-design,
philosophy-thinking, health-performance, reference-knowledge, other

## Rules

1. Choose exactly ONE primary category - the ability domain the book is
   really about, not a topic it merely mentions.
2. A book ABOUT decision making that uses poker examples is decision-making,
   not a gambling book. Follow the dominant teachable capability.
3. Add at most one subcategory and a handful of tags. Do not force-fit.
4. Confidence must be honest: 0.9+ only when the book announces itself
   unmistakably; below 0.5 means genuinely torn - say so in the rationale.
5. List plausible alternatives with their own confidences.
6. Ground the rationale in the book's actual content (quote chapter titles
   or themes, briefly).

## Output

Return ONLY a YAML object matching `schemas/classification.schema.json`:

```yaml
primary_category: decision-making
subcategory: uncertainty
confidence: 0.94
rationale: |
  <2-4 sentences grounded in the book's content>
alternative_categories:
  - category: psychology-behavior
    confidence: 0.63
tags: [probability, belief-updating]
method: agent
```
