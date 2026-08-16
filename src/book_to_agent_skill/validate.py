"""Skill directory validator: the quality gate before finalize/install."""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import jsonschema

from .paths import schemas_dir
from .provenance import check_reference_file, check_source_map
from .skillfile import (
    SKILL_LINE_LIMIT,
    check_frontmatter,
    has_todo,
    missing_sections,
    parse_frontmatter,
)
from .taxonomy import Taxonomy, TaxonomyError
from .util import read_text, read_yaml

REQUIRED_FILES = ["SKILL.md", "BOOK.yaml", "evals/cases.yaml"]
REQUIRED_REFERENCES = [
    "principles.md",
    "frameworks.md",
    "procedures.md",
    "examples.md",
    "limitations.md",
    "source-map.md",
]


@dataclass
class CheckResult:
    name: str
    ok: bool
    detail: str = ""


class SkillValidator:
    def __init__(self, skill_dir: Path, taxonomy: Optional[Taxonomy] = None):
        self.dir = Path(skill_dir)
        self.taxonomy = taxonomy or Taxonomy()
        self.results: List[CheckResult] = []

    def _check(self, name: str, ok: bool, detail: str = "") -> None:
        self.results.append(CheckResult(name=name, ok=ok, detail=detail))

    def run(self) -> bool:
        # 1. layout -------------------------------------------------------
        missing = [f for f in REQUIRED_FILES if not (self.dir / f).is_file()]
        refs_missing = [
            f for f in REQUIRED_REFERENCES
            if not (self.dir / "references" / f).is_file()
        ]
        detail = ""
        if missing:
            detail += "missing: " + ", ".join(missing) + ". "
        if refs_missing:
            detail += "missing references: " + ", ".join(refs_missing)
        self._check("layout", not missing and not refs_missing, detail.strip())
        if missing:
            return False  # nothing else can be checked meaningfully

        skill_md = read_text(self.dir / "SKILL.md")

        # In a pipeline workspace the staging dir is always named "skill";
        # the canonical name lives in BOOK.yaml.slug (and must match
        # frontmatter.name). Once installed, the directory itself is canonical.
        expected_name = self.dir.name
        staged = self.dir.name == "skill"
        if staged:
            staged_meta = read_yaml(self.dir / "BOOK.yaml") or {}
            expected_name = staged_meta.get("slug") or staged_meta.get("title") or "skill"

        # 2. frontmatter --------------------------------------------------
        meta, _body = parse_frontmatter(skill_md)
        fm_errors = check_frontmatter(meta, expected_name=expected_name)
        self._check(
            "frontmatter",
            not fm_errors,
            "; ".join(fm_errors),
        )

        # 3. BOOK.yaml ----------------------------------------------------
        category = None
        bookyaml_errors: List[str] = []
        try:
            book_meta = read_yaml(self.dir / "BOOK.yaml") or {}
            schema = json.loads(
                (schemas_dir() / "book_metadata.schema.json").read_text("utf-8")
            )
            jsonschema.validate(book_meta, schema)
            if book_meta.get("slug") != expected_name:
                bookyaml_errors.append(
                    f"slug '{book_meta.get('slug')}' != expected skill name '{expected_name}'"
                )
            category = book_meta.get("primary_category")
            if category and category not in self.taxonomy.by_id:
                bookyaml_errors.append(f"unknown primary_category '{category}'")
                category = None
        except jsonschema.ValidationError as e:
            bookyaml_errors.append(f"BOOK.yaml schema: {e.message}")
        except Exception as e:  # unreadable yaml etc.
            bookyaml_errors.append(f"BOOK.yaml: {e}")
        self._check("book-yaml", not bookyaml_errors, "; ".join(bookyaml_errors))

        # 4. required sections ---------------------------------------------
        if category:
            try:
                profile = self.taxonomy.profile(category)
                missing_secs = missing_sections(skill_md, profile["skill_sections"])
                self._check(
                    "skill-sections",
                    not missing_secs,
                    (
                        f"missing sections for profile '{category}': "
                        + ", ".join(missing_secs)
                    )
                    if missing_secs
                    else f"all {len(profile['skill_sections'])} sections present",
                )
            except TaxonomyError as e:
                self._check("skill-sections", False, str(e))
        else:
            self._check(
                "skill-sections", False, "skipped: BOOK.yaml has no valid category"
            )

        # 5. TODO markers ---------------------------------------------------
        todo_files: List[Path] = (
            [self.dir / "SKILL.md"] if (self.dir / "SKILL.md").is_file() else []
        )
        for ref in REQUIRED_REFERENCES:
            p = self.dir / "references" / ref
            if p.is_file():
                todo_files.append(p)
        evals_path = self.dir / "evals" / "cases.yaml"
        if evals_path.is_file():
            todo_files.append(evals_path)
        todo_hits = [str(p.relative_to(self.dir)) for p in todo_files if has_todo(read_text(p))]
        self._check(
            "draft-complete",
            not todo_hits,
            "unfinished TODO markers in: " + ", ".join(todo_hits)
            if todo_hits
            else "no TODO markers",
        )

        # 6. provenance ------------------------------------------------------
        provenance_errors: List[str] = []
        for ref in REQUIRED_REFERENCES:
            p = self.dir / "references" / ref
            if not p.is_file():
                continue  # already reported in layout
            if ref == "source-map.md":
                provenance_errors.extend(check_source_map(read_text(p)))
            else:
                for err in check_reference_file(ref, read_text(p)):
                    provenance_errors.append(err)
        self._check(
            "provenance",
            not provenance_errors,
            "; ".join(provenance_errors[:8])
            + (" ... (+%d more)" % (len(provenance_errors) - 8) if len(provenance_errors) > 8 else "")
            if provenance_errors
            else "content types + sources valid",
        )

        # 7. eval cases -------------------------------------------------------
        eval_errors: List[str] = []
        try:
            from .evalgen import check_eval_cases

            cases = read_yaml(evals_path)
            eval_errors = check_eval_cases(cases, self.taxonomy.eval_minimums())
        except Exception as e:
            eval_errors = [f"evals/cases.yaml unreadable: {e}"]
        self._check(
            "eval-cases",
            not eval_errors,
            "; ".join(eval_errors[:6]) if eval_errors else "counts + schema valid",
        )

        # 8. compactness (warning only) ----------------------------------------
        line_count = len(skill_md.splitlines())
        self._check(
            "compactness",
            True,
            f"{line_count} lines (soft limit {SKILL_LINE_LIMIT})"
            + (" - WARNING: trim into references/" if line_count > SKILL_LINE_LIMIT else ""),
        )

        return all(r.ok for r in self.results)

    # ------------------------------------------------------------------ report

    def report(self) -> str:
        lines = []
        for r in self.results:
            mark = "PASS" if r.ok else "FAIL"
            line = f"[{mark}] {r.name}"
            if r.detail:
                line += f" - {r.detail}"
            lines.append(line)
        return "\n".join(lines)
