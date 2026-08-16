import hashlib
import re
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

import yaml


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def word_count(text: str) -> int:
    return len(text.split())


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def slugify(text: str) -> str:
    """ASCII slug from arbitrary text; deterministic and filesystem-safe."""
    text = unicodedata.normalize("NFKD", text)
    ascii_text = text.encode("ascii", "ignore").decode("ascii").lower()
    ascii_text = re.sub(r"[^a-z0-9]+", "-", ascii_text)
    ascii_text = re.sub(r"-{2,}", "-", ascii_text).strip("-")
    ascii_text = ascii_text[:64].rstrip("-")
    return ascii_text or "book"


def read_yaml(path: Path) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def write_yaml(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)


def yaml_str(data: Any) -> str:
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def clean_excerpt(text: str, limit: int) -> str:
    """Lightly cleaned excerpt for digests."""
    snippet = " ".join(text.split())
    return snippet[:limit]
