"""Shared fixtures. Tests run against the repo checkout (editable install
or PYTHONPATH=src)."""

import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

EXAMPLE_BOOK = REPO_ROOT / "examples" / "books" / "the-decision-notebook.md"
EXAMPLE_SKILL = REPO_ROOT / "examples" / "output" / "decision-making" / "the-decision-notebook"


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return REPO_ROOT


@pytest.fixture(scope="session")
def example_book() -> Path:
    assert EXAMPLE_BOOK.exists(), "example book missing"
    return EXAMPLE_BOOK


@pytest.fixture(scope="session")
def example_skill() -> Path:
    assert EXAMPLE_SKILL.exists(), (
        "example skill missing - run `book2skill finalize --workspace "
        "examples/workspace --output examples/output` first"
    )
    return EXAMPLE_SKILL


@pytest.fixture()
def taxonomy():
    from book_to_agent_skill.taxonomy import Taxonomy

    return Taxonomy()
