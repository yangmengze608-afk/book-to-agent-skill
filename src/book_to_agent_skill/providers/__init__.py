"""Reasoning provider abstraction.

V1 defaults to `agent`: the calling agent (per the repo's root SKILL.md)
does the reasoning while the CLI handles deterministic steps. API providers
(openai, anthropic) are optional and experimental.
"""

from .base import NeedsAgentReasoning, ProviderError, ReasoningProvider
from .agent import AgentProvider
from .heuristic import HeuristicProvider


def get_provider(name: str):
    name = (name or "agent").lower()
    if name == "agent":
        return AgentProvider()
    if name == "heuristic":
        return HeuristicProvider()
    if name == "openai":
        from .openai_provider import OpenAIProvider

        return OpenAIProvider()
    if name == "anthropic":
        from .anthropic_provider import AnthropicProvider

        return AnthropicProvider()
    raise ProviderError(
        f"unknown provider '{name}' (expected agent | heuristic | openai | anthropic)"
    )


__all__ = [
    "ReasoningProvider",
    "NeedsAgentReasoning",
    "ProviderError",
    "AgentProvider",
    "HeuristicProvider",
    "get_provider",
]
