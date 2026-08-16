"""Taxonomy loading: categories + per-category distillation profiles."""

from pathlib import Path
from typing import Dict, List

import yaml

from .paths import profiles_dir, taxonomy_dir

_BASE_PROFILE = "_base.yaml"


class TaxonomyError(Exception):
    pass


class Taxonomy:
    def __init__(self, root: Path = None):
        # Accept either the repo root (contains taxonomy/) or the taxonomy dir.
        if root is None:
            root = taxonomy_dir()
        elif (root / "taxonomy" / "categories.yaml").exists():
            root = root / "taxonomy"
        self.root = root
        data = yaml.safe_load((root / "categories.yaml").read_text(encoding="utf-8"))
        self.categories: List[dict] = data["categories"]
        self.by_id: Dict[str, dict] = {c["id"]: c for c in self.categories}
        base_data = yaml.safe_load(
            (profiles_dir() / _BASE_PROFILE).read_text(encoding="utf-8")
        )
        self.base: dict = base_data["common"]
        self._profile_cache: Dict[str, dict] = {}

    # ------------------------------------------------------------------ ids

    def category_ids(self) -> List[str]:
        return [c["id"] for c in self.categories]

    def label(self, category_id: str) -> str:
        return self.by_id[category_id]["label"]

    def get(self, category_id: str) -> dict:
        try:
            return self.by_id[category_id]
        except KeyError:
            raise TaxonomyError(
                f"unknown category '{category_id}'. Valid: {', '.join(self.category_ids())}"
            )

    # -------------------------------------------------------------- profiles

    def profile(self, category_id: str) -> dict:
        """Merged distillation profile: base defaults + category overrides."""
        if category_id in self._profile_cache:
            return self._profile_cache[category_id]
        self.get(category_id)  # validate id
        path = profiles_dir() / f"{category_id}.yaml"
        if not path.exists():
            raise TaxonomyError(f"missing distillation profile: {path}")
        profile = yaml.safe_load(path.read_text(encoding="utf-8"))

        sections = list(self.base["skill_sections"])
        for extra in profile.get("skill_sections_extra", []) or []:
            if extra not in sections:
                sections.append(extra)
        override = profile.get("skill_sections_override")
        if override:
            sections = list(override)

        reference_files = dict(self.base["reference_files"])
        reference_files.update(profile.get("extra_reference_files", {}) or {})

        merged = {
            "category": category_id,
            "label": self.label(category_id),
            "focus": profile.get("focus", []),
            "epistemic_guardrails": profile.get("epistemic_guardrails", []),
            "example_trigger_questions": profile.get("example_trigger_questions", []),
            "example_anti_trigger_questions": profile.get(
                "example_anti_trigger_questions", []
            ),
            "skill_sections": sections,
            "reference_files": reference_files,
            "skill_sections_override": bool(override),
        }
        self._profile_cache[category_id] = merged
        return merged

    # ------------------------------------------------------------ validation

    def validate(self) -> List[str]:
        """Structural self-checks (used by tests and `book2skill` doctor)."""
        errors: List[str] = []
        ids = self.category_ids()
        if len(ids) != len(set(ids)):
            errors.append("duplicate category ids in categories.yaml")
        for c in self.categories:
            for key in ("id", "label", "description", "subcategories", "keywords"):
                if key not in c:
                    errors.append(f"category {c.get('id', '?')} missing key '{key}'")
        for cid in ids:
            if cid != "other" and not (profiles_dir() / f"{cid}.yaml").exists():
                errors.append(f"missing distillation profile for '{cid}'")
        for key in ("skill_sections", "reference_files", "epistemic_rules",
                    "eval_minimums"):
            if key not in self.base:
                errors.append(f"base profile missing '{key}'")
        return errors

    def eval_minimums(self) -> dict:
        return dict(self.base["eval_minimums"])
