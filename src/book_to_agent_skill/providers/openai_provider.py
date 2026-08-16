"""OpenAI-compatible API provider (experimental, optional).

Uses stdlib urllib only. Configure via environment:
  OPENAI_API_KEY   (required)
  OPENAI_BASE_URL  (default https://api.openai.com/v1)
  OPENAI_MODEL     (default gpt-4o-mini)
"""

import json
import os
import re
import urllib.error
import urllib.request

from ..paths import load_prompt
from .base import ProviderError, ReasoningProvider


def _chat_json(system: str, user: str, max_tokens: int = 8000) -> dict:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ProviderError("OPENAI_API_KEY is not set")
    base = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "response_format": {"type": "json_object"},
        "max_tokens": max_tokens,
        "temperature": 0.2,
    }
    req = urllib.request.Request(
        f"{base}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as e:
        raise ProviderError(f"openai request failed: {e}") from e
    try:
        content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as e:
        raise ProviderError(f"openai response malformed: {data}") from e
    return _loads_lenient(content)


def _loads_lenient(content: str):
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        m = re.search(r"\{.*\}|\[.*\]", content, re.DOTALL)
        if m:
            return json.loads(m.group(0))
        raise ProviderError(f"provider returned non-JSON content: {content[:300]}")


class OpenAIProvider(ReasoningProvider):
    name = "openai"

    def classify(self, book_digest: str, taxonomy) -> dict:
        system = load_prompt("classify.md")
        user = (
            "Allowed categories: "
            + ", ".join(taxonomy.category_ids())
            + "\n\nBOOK DIGEST:\n"
            + book_digest
        )
        result = _chat_json(system, user, max_tokens=1500)
        result.setdefault("method", "openai")
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
