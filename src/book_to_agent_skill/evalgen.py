"""Eval generation context, work order, and validation of cases.yaml."""

import json
from typing import List

import jsonschema

from .models import Book
from .paths import schemas_dir, load_prompt
from .taxonomy import Taxonomy
from .util import yaml_str


def eval_context(book: Book, cls: dict, skill_md_excerpt: str) -> dict:
    return {
        "book": {"title": book.title_hint, "author": book.author_hint},
        "category": cls["primary_category"],
        "skill_md_excerpt": skill_md_excerpt[:4000],
        "reminder": (
            "Minimum counts: 5 positive_trigger, 5 negative_trigger, "
            "5 application, 3 edge_case. Types exactly as in "
            "schemas/eval_cases.schema.json."
        ),
    }


def eval_workorder(book: Book, cls: dict, skill_md_excerpt: str) -> str:
    return f"""# Work Order 03 - Eval Cases

Author `skill/evals/cases.yaml` for the skill you just wrote.
Full guide: prompts/evals.md. Schema: schemas/eval_cases.schema.json.

## Eval context

```yaml
{yaml_str(eval_context(book, cls, skill_md_excerpt))}
```

## Requirements

- >= 5 positive_trigger, >= 5 negative_trigger (with must_avoid),
  >= 5 application, >= 3 edge_case
- ids: trigger-NNN / anti-NNN / application-NNN / edge-NNN
- prompts read like real user messages; expected entries are observable
  behaviors; do not leak answers into prompts

## When done

`book2skill finalize --workspace <workspace>` validates and installs.
"""


def check_eval_cases(cases, minimums: dict) -> List[str]:
    errors: List[str] = []
    if not isinstance(cases, list):
        return ["evals/cases.yaml: must be a YAML list of cases"]
    schema = json.loads(
        (schemas_dir() / "eval_cases.schema.json").read_text(encoding="utf-8")
    )
    try:
        jsonschema.validate(cases, schema)
    except jsonschema.ValidationError as e:
        return [f"eval cases schema: {e.message}"]

    ids = [c["id"] for c in cases]
    if len(ids) != len(set(ids)):
        dupes = sorted({i for i in ids if ids.count(i) > 1})
        errors.append(f"duplicate eval ids: {dupes}")

    counts = {}
    for c in cases:
        counts[c["type"]] = counts.get(c["type"], 0) + 1
    for case_type, minimum in minimums.items():
        got = counts.get(case_type, 0)
        if got < minimum:
            errors.append(f"eval type '{case_type}': {got} < minimum {minimum}")

    for c in cases:
        if c["type"] == "negative_trigger" and not c.get("must_avoid"):
            errors.append(
                f"{c['id']}: negative_trigger cases require 'must_avoid' behaviors"
            )
    return errors
