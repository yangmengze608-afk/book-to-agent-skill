"""Anthropic API provider (experimental, optional).

Uses stdlib urllib only. Configure via environment:
  ANTHROPIC_API_KEY  (required)
  ANTHROPIC_MODEL    (default claude-sonnet-4-5)
"""

import json
import os
import re
import urllib.error
import urllib.request

from ..paths import load_prompt
from .openai_provider import _loads_lenient
from .base import ProviderError, ReasoningProvider


def _chat_json(system: str, user: str, max_tokens: int = 8000) -> dict:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ProviderError("ANTHROPIC_API_KEY is not set")
    model = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-5")
    payload = {
        "model": model,
        "system": system
        + "\n\nAlways respond with a single JSON object and nothing else.",
        "messages": [{"role": "user", "content": user}],
        "max_tokens": max_tokens,
        "temperature": 0.2,
    }
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as e:
        raise ProviderError(f"anthropic request failed: {e}") from e
    try:
        content = data["content"][0]["text"]
    except (KeyError, IndexError) as e:
        raise ProviderError(f"anthropic response malformed: {data}") from e
    return _loads_lenient(content)


class AnthropicProvider(ReasoningProvider):
    name = "anthropic"

    def classify(self, book_digest: str, taxonomy) -> dict:
        system = load_prompt("classify.md")
        user = (
            "Allowed categories: "
            + ", ".join(taxonomy.category_ids())
            + "\n\nBOOK DIGEST:\n"
            + book_digest
        )
        result = _chat_json(system, user, max_tokens=1500)
        result.setdefault("method", "anthropic")
        return result

    def distill(self, request: dict) -> dict:
        system = (
            load_prompt("distill_common.md")
            + "\n\n"
            + load_prompt("distill_skill.md")
        )
        user = json.dumps(request, ensure_ascii=False)[:120000]
        return _chat_json(system, user, max_tokens=12000)

    def evals(self, context: dict) -> list:
        system = load_prompt("evals.md")
        user = json.dumps(context, ensure_ascii=False)[:40000]
        result = _chat_json(system, user, max_tokens=8000)
        if isinstance(result, dict):
            for key in ("cases", "eval_cases", "evals"):
                if key in result:
                    return result[key]
        return result
