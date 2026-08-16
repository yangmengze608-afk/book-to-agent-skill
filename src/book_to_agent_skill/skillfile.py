"""SKILL.md parsing and structural checks."""

import re
from typing import Dict, List, Optional, Tuple

import yaml

FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?", re.DOTALL)
SECTION_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)
TODO_RE = re.compile(r"\bTODO\b")

SKILL_LINE_LIMIT = 400  # soft compactness guard


def parse_frontmatter(md_text: str) -> Tuple[Optional[dict], str]:
    m = FRONTMATTER_RE.match(md_text)
    if not m:
        return None, md_text
    try:
        meta = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return None, md_text
    return meta, md_text[m.end() :]


def section_names(md_text: str) -> List[str]:
    return [s.strip() for s in SECTION_RE.findall(md_text)]


def missing_sections(md_text: str, required: List[str]) -> List[str]:
    present = {s.lower().rstrip(":") for s in section_names(md_text)}
    return [r for r in required if r.lower().rstrip(":") not in present]


def has_todo(text: str) -> bool:
    return bool(TODO_RE.search(text))


def check_frontmatter(meta: Optional[dict], expected_name: str = None) -> List[str]:
    errors: List[str] = []
    if not meta:
        return ["SKILL.md is missing YAML frontmatter (--- name: ... ---)"]
    name = meta.get("name")
    if not name or not isinstance(name, str):
        errors.append("frontmatter: 'name' is required")
    elif expected_name and name != expected_name:
        errors.append(f"frontmatter name '{name}' != skill directory '{expected_name}'")
    desc = meta.get("description")
    if not desc or not isinstance(desc, str) or len(desc.strip()) < 20:
        errors.append("frontmatter: 'description' must be a string of >= 20 chars")
    return errors
