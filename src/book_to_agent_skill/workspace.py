"""Workspace: the on-disk state machine for one book-to-skill run."""

from pathlib import Path
from typing import Optional

import yaml

from .util import read_yaml, write_yaml


class Workspace:
    def __init__(self, root: Path):
        self.root = Path(root)

    # ------------------------------------------------------------- paths

    @property
    def book_dir(self) -> Path:
        return self.root / "book"

    @property
    def book_text(self) -> Path:
        return self.book_dir / "text.md"

    @property
    def source_meta(self) -> Path:
        return self.book_dir / "source_meta.yaml"

    @property
    def structure(self) -> Path:
        return self.book_dir / "structure.yaml"

    @property
    def workorder_dir(self) -> Path:
        return self.root / "workorder"

    @property
    def classification(self) -> Path:
        return self.root / "classification.yaml"

    @property
    def classification_workorder(self) -> Path:
        return self.workorder_dir / "01-classification.md"

    @property
    def distill_workorder(self) -> Path:
        return self.workorder_dir / "02-distillation.md"

    @property
    def eval_workorder(self) -> Path:
        return self.workorder_dir / "03-evals.md"

    @property
    def skill_dir(self) -> Path:
        return self.root / "skill"

    @property
    def state_path(self) -> Path:
        return self.root / "state.yaml"

    # ------------------------------------------------------------- actions

    def ensure(self) -> "Workspace":
        for d in (self.root, self.book_dir, self.workorder_dir):
            d.mkdir(parents=True, exist_ok=True)
        return self

    def load_state(self) -> dict:
        if self.state_path.exists():
            data = read_yaml(self.state_path)
            return data if isinstance(data, dict) else {}
        return {}

    def save_state(self, **fields) -> None:
        state = self.load_state()
        state.update(fields)
        write_yaml(self.state_path, state)

    def load_classification(self) -> Optional[dict]:
        if self.classification.exists():
            data = read_yaml(self.classification)
            if isinstance(data, dict) and data.get("primary_category"):
                return data
        return None
