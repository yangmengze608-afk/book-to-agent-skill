"""4. Invalid category / classification validation + heuristic behavior."""

import pytest

from book_to_agent_skill.classify import (
    HEURISTIC_CONFIDENCE_CAP,
    heuristic_classify,
    validate_classification,
)
from book_to_agent_skill.ingest import ingest


def _valid_classification(**over):
    base = {
        "primary_category": "decision-making",
        "subcategory": "uncertainty",
        "confidence": 0.9,
        "rationale": "The book teaches decision-making under uncertainty.",
        "alternative_categories": [
            {"category": "psychology-behavior", "confidence": 0.6}
        ],
        "tags": ["probability"],
        "method": "agent",
    }
    base.update(over)
    return base


def test_valid_classification_passes(taxonomy):
    assert validate_classification(_valid_classification(), taxonomy) == []


def test_invalid_primary_category(taxonomy):
    errors = validate_classification(
        _valid_classification(primary_category="not-a-category"), taxonomy
    )
    assert any("unknown primary_category" in e for e in errors)


def test_invalid_subcategory(taxonomy):
    errors = validate_classification(
        _valid_classification(subcategory="deep-sea-diving"), taxonomy
    )
    assert any("subcategory" in e for e in errors)


def test_heuristic_confidence_capped(taxonomy):
    errors = validate_classification(
        _valid_classification(method="heuristic", confidence=0.99), taxonomy
    )
    assert any("cap" in e for e in errors)
    assert HEURISTIC_CONFIDENCE_CAP == 0.6


def test_invalid_alternative_category(taxonomy):
    errors = validate_classification(
        _valid_classification(
            alternative_categories=[{"category": "bogus", "confidence": 0.5}]
        ),
        taxonomy,
    )
    assert any("alternative" in e for e in errors)


def test_schema_rejects_missing_fields(taxonomy):
    bad = _valid_classification()
    del bad["rationale"]
    errors = validate_classification(bad, taxonomy)
    assert errors and "schema" in errors[0]


def test_heuristic_on_example_book(example_book, taxonomy):
    """The heuristic must classify the example book into a sane category
    with capped confidence and an honest rationale."""
    book = ingest(example_book)
    cls = heuristic_classify(book, taxonomy)
    assert cls.primary_category in taxonomy.category_ids()
    assert 0 < cls.confidence <= HEURISTIC_CONFIDENCE_CAP
    assert "heuristic" in cls.rationale
