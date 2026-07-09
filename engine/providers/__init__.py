"""
Providers — AI provider integrations.

Provider-specific code is isolated here. The rest of the engine
remains unaware of which provider is being used.

Current: Fireworks AI + Gemini.
Future:  OpenAI, Anthropic, local inference, etc.

Usage:
    from engine.providers import create_provider

    provider = create_provider()          # uses config
    scene = provider.generate_scene_description(messages)
    captions = provider.generate_captions(messages)
"""

from engine.providers.base import BaseProvider
from engine.providers.factory import create_provider

__all__ = [
    "BaseProvider",
    "create_provider",
]
