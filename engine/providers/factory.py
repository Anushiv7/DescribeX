"""
Provider factory — selects and instantiates the configured AI provider.

The factory reads ``EngineConfig.provider`` to determine which concrete
provider to create.  The CaptionEngine calls :func:`create_provider`
and receives a :class:`BaseProvider` — it never imports a concrete
provider class directly.

Supported values for ``DESCRIBEX_PROVIDER``:

* ``"fireworks"`` — Fireworks AI (OpenAI-compatible API)
* ``"gemini"``    — Google Gemini (google-genai SDK)
"""

from __future__ import annotations

from engine.providers.base import BaseProvider
from engine.utils.config import EngineConfig, get_config
from engine.utils.exceptions import ProviderError
from engine.utils.logging import get_logger

logger = get_logger(__name__)


def create_provider(config: EngineConfig | None = None) -> BaseProvider:
    """Instantiate the AI provider specified in the configuration.

    Args:
        config: Optional runtime configuration.  When *None* the shared
            singleton from :func:`get_config` is used.

    Returns:
        A ready-to-use :class:`BaseProvider` instance.

    Raises:
        ProviderError: If the configured provider name is unknown or
            if the provider fails to initialise (e.g. missing API key).
    """
    cfg = config or get_config()
    provider_name = cfg.provider.lower().strip()

    logger.info("Creating provider: '%s'", provider_name)

    if provider_name == "fireworks":
        from engine.providers.fireworks import FireworksProvider

        return FireworksProvider(cfg)

    if provider_name == "gemini":
        from engine.providers.gemini import GeminiProvider

        return GeminiProvider(cfg)

    raise ProviderError(
        f"Unknown provider '{provider_name}'. "
        f"Set DESCRIBEX_PROVIDER to one of: fireworks, gemini"
    )
