"""Distillation: profile selection, skill scaffolding, work orders."""

from pathlib import Path
from typing import Dict, List

from .models import Book
from .taxonomy import Taxonomy
from .util import now_iso, slugify, write_text, write_yaml, yaml_str

SKILL_SOFT_LINE_LIMIT = 400


# ------------------------------------------------------------------ BOOK.yaml

def build_book_yaml(
    book: Book, cls: dict, slug: str, distillation_version: str = "1.0"
) -> dict:
    return {
        "title": book.title_hint or slug,
        "author": book.author_hint or "unknown",
        "primary_category": cls["primary_category"],
        "subcategory": cls.get("subcategory"),
        "tags": cls.get("tags", []),
        "classification_confidence": cls["confidence"],
        "alternative_categories": cls.get("alternative_categories", []),
        "book_type": "monograph",
        "language": "en",
        "source_format": book.fmt,
        "distillation_version": distillation_version,
        "generated_at": now_iso(),
        "slug": slug,
        "source_metadata": book.source_meta.to_dict(),
    }


# ----------------------------------------------------------------- scaffolds

def skill_skeleton(slug: str, title: str, profile: dict) -> str:
    lines = [
        "---",
        f"name: {slug}",
        f"description: TODO - 1-3 sentences on what this skill (from '{title}')"
        " makes the agent good at, and when to use it.",
        "---",
        "",
    ]
    for section in profile["skill_sections"]:
        lines.append(f"## {section}")
        lines.append(
            f"> TODO(agent): fill this section per prompts/distill_skill.md "
            f"and the '{profile['category']}' distillation profile."
        )
        lines.append("")
    return "\n".join(lines)


def reference_skeleton(name: str, description: str) -> str:
    return f"""# {name}

> Purpose: {description}

Entry format (enforced by the validator):

```markdown
### P1. Short imperative title
- type: SOURCE FACT            <!-- or AUTHOR CLAIM / EVIDENCE / DISTILLER INFERENCE -->
- source: chapter 3, section "Resulting"   <!-- required for the 3 source types; never invent pages -->
- source_confidence: high      <!-- high | medium | low -->
- derived_from: P2, F1         <!-- required for DISTILLER INFERENCE instead of source -->

Operational body: what this means and how to apply it.
```
"""


def scaffold_skill_dir(
    skill_dir: Path, book: Book, cls: dict, taxonomy: Taxonomy
) -> Dict[str, Path]:
    """Create the draft skill tree the agent (or API provider) fills in."""
    slug = slugify(book.title_hint or book.path.stem)
    profile = taxonomy.profile(cls["primary_category"])

    written: Dict[str, Path] = {}
    skill_dir.mkdir(parents=True, exist_ok=True)

    skill_md = skill_dir / "SKILL.md"
    write_text(skill_md, skill_skeleton(slug, book.title_hint or slug, profile))
    written["SKILL.md"] = skill_md

    refs_dir = skill_dir / "references"
    refs_dir.mkdir(exist_ok=True)
    for name, description in profile["reference_files"].items():
        path = refs_dir / name
        write_text(path, reference_skeleton(name, description))
        written[f"references/{name}"] = path

    evals_dir = skill_dir / "evals"
    evals_dir.mkdir(exist_ok=True)
    evals_path = evals_dir / "cases.yaml"
    if not evals_path.exists():
        write_text(
            evals_path,
            "# TODO(agent): eval cases per prompts/evals.md\n"
            "# Minimum: 5 positive_trigger, 5 negative_trigger, 5 application, 3 edge_case\n[]\n",
        )
    written["evals/cases.yaml"] = evals_path

    write_yaml(skill_dir / "BOOK.yaml", build_book_yaml(book, cls, slug))
    written["BOOK.yaml"] = skill_dir / "BOOK.yaml"
    return written


# ------------------------------------------------------------------ requests

def distill_request(book: Book, cls: dict, taxonomy: Taxonomy) -> dict:
    """Payload handed to API providers (and embedded into work orders)."""
    profile = taxonomy.profile(cls["primary_category"])
    return {
        "book": {
            "title": book.title_hint,
            "author": book.author_hint,
            "words": book.words,
            "chapters": [
                {"index": c.index, "title": c.title, "words": c.words(book.text),
                 "synthetic": c.synthetic}
                for c in book.chapters
            ],
        },
        "classification": cls,
        "profile": profile,
        "output_contract": {
            "skill_md": (
                "Full SKILL.md text: YAML frontmatter (name=<slug>, description) "
                "then exactly these sections: "
                + "; ".join(profile["skill_sections"])
            ),
            "references": {
                name: f"Markdown content for {name}: {desc}"
                for name, desc in profile["reference_files"].items()
            },
        },
        "book_digest": book.digest(28000),
    }


# ---------------------------------------------------------------- work orders

def classification_workorder(book: Book, taxonomy: Taxonomy, heuristic: dict) -> str:
    return f"""# Work Order 01 - Classification

Classify the book, then write `classification.yaml` in the workspace root
(schema: schemas/classification.schema.json).

## Book digest

```
{book.digest(12000)}
```

## Heuristic pre-classification (hint only - confirm or replace)

```yaml
{yaml_str(heuristic)}
```

## Instructions

1. Read the digest above (and workspace/book/text.md as needed).
2. Pick exactly ONE primary category from taxonomy/categories.yaml:
   {", ".join(taxonomy.category_ids())}
3. Judge honestly - confidence below 0.5 means genuinely torn.
4. Write classification.yaml (fields per the schema; set method: agent).
5. Run: `book2skill distill --workspace <workspace>` to validate and scaffold.
"""


def distillation_workorder(book: Book, cls: dict, taxonomy: Taxonomy) -> str:
    profile = taxonomy.profile(cls["primary_category"])
    return f"""# Work Order 02 - Distillation ({profile['label']})

The skill scaffold is in `skill/`. Fill it in. This work order is
self-contained; the full rules live in prompts/distill_common.md and
prompts/distill_skill.md (read them first if unfamiliar).

## Classification (already validated)

```yaml
{yaml_str(cls)}
```

## Category profile: {profile['category']}

Extract with THIS focus:

{yaml_str({"focus": profile["focus"], "epistemic_guardrails": profile["epistemic_guardrails"]})}

## Required SKILL.md sections

{chr(10).join("- " + s for s in profile["skill_sections"])}

## Required references files

{chr(10).join(f"- {name}: {desc}" for name, desc in profile["reference_files"].items())}

## Book digest (full text: workspace/book/text.md)

```
{book.digest(28000)}
```

## When done

Run `book2skill validate <workspace>/skill` to check, then
`book2skill finalize --workspace <workspace>` to install.
"""


def apply_provider_result(skill_dir: Path, result: dict, slug_hint: str) -> None:
    """Write an API provider's distill() result into the skill dir."""
    skill_md = result.get("skill_md")
    if not skill_md or not isinstance(skill_md, str):
        raise ValueError("provider result missing 'skill_md'")
    write_text(skill_dir / "SKILL.md", skill_md)
    references = result.get("references") or {}
    if not isinstance(references, dict) or not references:
        raise ValueError("provider result missing 'references' mapping")
    refs_dir = skill_dir / "references"
    refs_dir.mkdir(exist_ok=True)
    for name, content in references.items():
        safe = Path(name).name  # no traversal
        write_text(refs_dir / safe, str(content))
