import os
from pathlib import Path

_PACKAGE_FILE = Path(__file__).resolve()


def repo_root() -> Path:
    """Locate the repository root that carries taxonomy/, schemas/, prompts/.

    Resolution order:
    1. $B2A_ROOT (useful when the package is installed elsewhere)
    2. walk up from this file (covers editable installs and repo checkouts)
    """
    env = os.environ.get("B2A_ROOT")
    if env:
        root = Path(env)
        if (root / "taxonomy" / "categories.yaml").exists():
            return root
        raise RuntimeError(f"B2A_ROOT={env} does not contain taxonomy/categories.yaml")

    for parent in _PACKAGE_FILE.parents:
        if (parent / "taxonomy" / "categories.yaml").exists() and (
            parent / "pyproject.toml"
        ).exists():
            return parent
    raise RuntimeError(
        "Could not locate the book-to-agent-skill repo root "
        "(taxonomy/categories.yaml). If you installed the package outside the "
        "repo, set B2A_ROOT to the repo checkout path."
    )


def taxonomy_dir() -> Path:
    return repo_root() / "taxonomy"


def profiles_dir() -> Path:
    return taxonomy_dir() / "distillation_profiles"


def schemas_dir() -> Path:
    return repo_root() / "schemas"


def prompts_dir() -> Path:
    return repo_root() / "prompts"


def load_prompt(name: str) -> str:
    path = prompts_dir() / name
    if not path.exists():
        raise FileNotFoundError(f"prompt not found: {path}")
    return path.read_text(encoding="utf-8")
