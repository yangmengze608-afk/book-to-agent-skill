"""5. Missing provenance + content-type rules in references/*.md."""

from book_to_agent_skill.provenance import (
    check_reference_file,
    check_source_map,
    parse_entries,
)


def test_valid_entry_passes():
    entry = """### P%d. A principle
- type: AUTHOR CLAIM
- source: chapter 1, section "Bets"
- source_confidence: high

Body text.
"""
    md = "".join(entry % i for i in (1, 2, 3))  # principles.md minimum is 3
    assert check_reference_file("principles.md", md) == []


def test_missing_source_fails():
    md = """### P1. A principle
- type: AUTHOR CLAIM
- source_confidence: high

Body.
"""
    errors = check_reference_file("principles.md", md)
    assert any("requires '- source:" in e for e in errors)


def test_missing_source_confidence_fails():
    md = """### P1. A principle
- type: EVIDENCE
- source: chapter 2, section "Data"

Body.
"""
    errors = check_reference_file("principles.md", md)
    assert any("source_confidence" in e for e in errors)


def test_invalid_type_fails():
    md = """### P1. A principle
- type: WILD GUESS
- source: chapter 1, section "Bets"
- source_confidence: high

Body.
"""
    errors = check_reference_file("principles.md", md)
    assert any("invalid type" in e for e in errors)


def test_distiller_inference_requires_derived_from():
    md = """### P1. A principle
- type: DISTILLER INFERENCE

Body.
"""
    errors = check_reference_file("principles.md", md)
    assert any("derived_from" in e for e in errors)


def test_missing_type_fails():
    md = """### P1. A principle

Body.
"""
    errors = check_reference_file("principles.md", md)
    assert any("missing '- type:'" in e for e in errors)


def test_duplicate_entry_ids_fail():
    md = """### P1. First
- type: AUTHOR CLAIM
- source: chapter 1, section "A"
- source_confidence: high

### P1. Duplicate
- type: AUTHOR CLAIM
- source: chapter 2, section "B"
- source_confidence: high
"""
    errors = check_reference_file("principles.md", md)
    assert any("duplicate entry ids" in e for e in errors)


def test_below_minimum_entries_fails():
    md = """### P1. Only one
- type: AUTHOR CLAIM
- source: chapter 1, section "A"
- source_confidence: high
"""
    errors = check_reference_file("principles.md", md)  # minimum is 3
    assert any("< minimum" in e for e in errors)


def test_fenced_code_blocks_are_ignored():
    """Format documentation inside ``` fences must not be parsed as
    entries (scaffold templates embed example entries)."""
    md = """# file

```markdown
### P1. Example from template
- type: SOURCE FACT
```

### P1. Real entry
- type: AUTHOR CLAIM
- source: chapter 1, section "A"
- source_confidence: high

Real body.
"""
    entries = parse_entries(md)
    assert [e.entry_id for e in entries] == ["P1"]
    assert entries[0].type == "AUTHOR CLAIM"


def test_source_map_requires_legend_and_chapters():
    assert check_source_map(
        "SOURCE FACT, AUTHOR CLAIM, EVIDENCE, DISTILLER INFERENCE; "
        "entries map to chapter N"
    ) == []
    errors = check_source_map("just some text")
    assert len(errors) >= 2
