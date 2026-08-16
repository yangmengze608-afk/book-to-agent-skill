"""Provenance: parse and check content-type/source annotations in references.

Canonical entry format inside references/*.md:

    ### P1. Separate decision quality from outcome quality
    - type: SOURCE FACT
    - source: chapter 3, section "Resulting"
    - source_confidence: high
    <operational body text>

Rules enforced:
- type must be one of the four content types
- SOURCE FACT / AUTHOR CLAIM / EVIDENCE require `source`
- DISTILLER INFERENCE requires `derived_from` (ids of entries it builds on)
- sourced entries require source_confidence in {high, medium, low}
"""

import re
from dataclasses import dataclass, field
from typing import List, Optional

CONTENT_TYPES = ("SOURCE FACT", "AUTHOR CLAIM", "EVIDENCE", "DISTILLER INFERENCE")
SOURCE_TYPES = ("SOURCE FACT", "AUTHOR CLAIM", "EVIDENCE")
CONFIDENCE_LEVELS = ("high", "medium", "low")

ENTRY_RE = re.compile(r"^##+\s+([A-Z]{1,3}\d+)\.?\s*[-:\u2014]?\s*(.+?)\s*$", re.MULTILINE)
FIELD_RES = {
    "type": re.compile(r"^-\s+type:\s*(.+?)\s*$", re.MULTILINE),
    "source": re.compile(r"^-\s+source:\s*(.+?)\s*$", re.MULTILINE),
    "source_confidence": re.compile(r"^-\s+source_confidence:\s*(.+?)\s*$", re.MULTILINE),
    "derived_from": re.compile(r"^-\s+derived_from:\s*(.+?)\s*$", re.MULTILINE),
}

# Minimum annotated entries per core reference file.
MIN_ENTRIES = {
    "principles.md": 3,
    "frameworks.md": 2,
    "procedures.md": 2,
    "examples.md": 1,
    "limitations.md": 1,
}


@dataclass
class Entry:
    entry_id: str
    title: str
    type: Optional[str] = None
    source: Optional[str] = None
    source_confidence: Optional[str] = None
    derived_from: Optional[str] = None
    errors: List[str] = field(default_factory=list)


def parse_entries(md_text: str) -> List[Entry]:
    md_text = re.sub(r"```.*?```", "", md_text, flags=re.DOTALL)  # ignore format docs/examples
    marks = [(m.group(1), m.group(2), m.start(), m.end()) for m in ENTRY_RE.finditer(md_text)]
    entries: List[Entry] = []
    for i, (eid, title, start, body_start) in enumerate(marks):
        end = marks[i + 1][2] if i + 1 < len(marks) else len(md_text)
        body = md_text[body_start:end]
        entry = Entry(entry_id=eid, title=title)

        def field_of(name: str) -> Optional[str]:
            m = FIELD_RES[name].search(body)
            return m.group(1) if m else None

        entry.type = field_of("type")
        entry.source = field_of("source")
        entry.source_confidence = field_of("source_confidence")
        entry.derived_from = field_of("derived_from")
        entries.append(entry)
    return entries


def check_entry(entry: Entry) -> List[str]:
    errors = list(entry.errors)
    if not entry.type:
        errors.append(f"{entry.entry_id}: missing '- type:' line")
    elif entry.type not in CONTENT_TYPES:
        errors.append(
            f"{entry.entry_id}: invalid type '{entry.type}' (must be one of {CONTENT_TYPES})"
        )
    else:
        if entry.type in SOURCE_TYPES:
            if not entry.source:
                errors.append(
                    f"{entry.entry_id}: {entry.type} requires '- source: chapter N, section \"...\"' "
                    f"(never invent page numbers)"
                )
            if not entry.source_confidence:
                errors.append(f"{entry.entry_id}: requires '- source_confidence:' (high/medium/low)")
        if entry.type == "DISTILLER INFERENCE" and not entry.derived_from:
            errors.append(
                f"{entry.entry_id}: DISTILLER INFERENCE requires '- derived_from:' "
                f"(ids of the entries it was derived from)"
            )
    if entry.source_confidence and entry.source_confidence not in CONFIDENCE_LEVELS:
        errors.append(
            f"{entry.entry_id}: source_confidence '{entry.source_confidence}' "
            f"must be high/medium/low"
        )
    return errors


def check_reference_file(name: str, md_text: str) -> List[str]:
    """Full check for one reference file: entries, types, provenance, minimums."""
    errors: List[str] = []
    entries = parse_entries(md_text)
    if not entries:
        errors.append(f"references/{name}: no annotated entries found (need '### ID. Title' + '- type:')")
        return errors
    for entry in entries:
        errors.extend(check_entry(entry))
    minimum = MIN_ENTRIES.get(name)
    if minimum and len(entries) < minimum:
        errors.append(f"references/{name}: {len(entries)} entries < minimum {minimum}")
    ids = [e.entry_id for e in entries]
    if len(ids) != len(set(ids)):
        dupes = sorted({i for i in ids if ids.count(i) > 1})
        errors.append(f"references/{name}: duplicate entry ids {dupes}")
    return errors


def check_source_map(md_text: str) -> List[str]:
    errors: List[str] = []
    for t in CONTENT_TYPES:
        if t not in md_text:
            errors.append(f"references/source-map.md: missing legend entry for '{t}'")
    if "chapter" not in md_text.lower():
        errors.append("references/source-map.md: should map entries to chapters/sections")
    return errors
