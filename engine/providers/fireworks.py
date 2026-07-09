"""
Fireworks AI provider implementation.

Uses the OpenAI-compatible API at ``https://api.fireworks.ai/inference/v1``.
Model IDs are read exclusively from :class:`EngineConfig` — never hardcoded.

If Fireworks reports that a model requires a dedicated deployment or is
otherwise unavailable, a clear :class:`ProviderError` is raised.  The
provider never silently switches models or creates deployments.
"""

from __future__ import annotations

import time

from openai import APIConnectionError, APIStatusError, APITimeoutError, OpenAI

from engine.providers.base import BaseProvider
from engine.utils.config import EngineConfig, get_config
from engine.utils.exceptions import ProviderError
from engine.utils.logging import get_logger

logger = get_logger(__name__)

# Fireworks AI OpenAI-compatible endpoint.
_FIREWORKS_BASE_URL = "https://api.fireworks.ai/inference/v1"

# Retry parameters.
_MAX_RETRIES = 3
_RETRY_BASE_DELAY_SECONDS = 2


class FireworksProvider(BaseProvider):
    """Fireworks AI provider using the OpenAI-compatible chat completions API."""

    def __init__(self, config: EngineConfig | None = None) -> None:
        self._config = config or get_config()

        if not self._config.fireworks_api_key:
            raise ProviderError(
                "Fireworks API key is not configured. "
                "Set DESCRIBEX_FIREWORKS_API_KEY in your environment or .env file."
            )

        self._client = OpenAI(
            base_url=_FIREWORKS_BASE_URL,
            api_key=self._config.fireworks_api_key,
            timeout=float(self._config.request_timeout_seconds),
        )
        logger.info("FireworksProvider initialized.")

    # ------------------------------------------------------------------
    # Public interface (implements BaseProvider)
    # ------------------------------------------------------------------

    def generate_scene_description(self, messages: list[dict]) -> str:
        """Send a vision prompt to Fireworks and return the scene description."""
        model_id = self._config.vision_model_id
        logger.info(
            "Generating scene description via Fireworks (model=%s)", model_id
        )
        return self._call(model_id, messages)

    def generate_captions(self, messages: list[dict]) -> str:
        """Send a text prompt to Fireworks and return raw caption JSON."""
        model_id = self._config.text_model_id
        logger.info(
            "Generating captions via Fireworks (model=%s)", model_id
        )
        return self._call(model_id, messages)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _call(self, model_id: str, messages: list[dict]) -> str:
        """Execute a chat completion request with retry logic.

        Raises:
            ProviderError: On any unrecoverable failure including model
                unavailability, deployment requirements, auth failures,
                or exhausted retries.
        """
        if not model_id:
            raise ProviderError(
                "No model ID configured. "
                "Set DESCRIBEX_VISION_MODEL_ID and DESCRIBEX_TEXT_MODEL_ID "
                "in your environment or .env file."
            )

        last_error: Exception | None = None

        for attempt in range(1, _MAX_RETRIES + 1):
            try:
                logger.debug(
                    "Fireworks API call attempt %d/%d (model=%s)",
                    attempt,
                    _MAX_RETRIES,
                    model_id,
                )
                response = self._client.chat.completions.create(
                    model=model_id,
                    messages=messages,
                    temperature=self._config.temperature,
                )
                content = response.choices[0].message.content
                if content is None:
                    raise ProviderError(
                        f"Fireworks returned an empty response for model {model_id}."
                    )
                logger.info("Fireworks API call succeeded (model=%s).", model_id)
                return content

            except APIStatusError as exc:
                last_error = exc
                # Surface clear errors for deployment-gated or unavailable models.
                status = exc.status_code
                body = str(exc.body) if exc.body else ""

                if status == 404:
                    raise ProviderError(
                        f"Model '{model_id}' was not found on Fireworks AI. "
                        f"Verify the model ID is correct and available. "
                        f"Server response: {body}"
                    ) from exc

                if status in (402, 403):
                    raise ProviderError(
                        f"Model '{model_id}' requires a dedicated deployment "
                        f"or is not accessible with your current plan. "
                        f"Fireworks returned HTTP {status}. "
                        f"Server response: {body}"
                    ) from exc

                if status == 429:
                    # Rate limited — back off and retry.
                    delay = _RETRY_BASE_DELAY_SECONDS * attempt
                    logger.warning(
                        "Rate limited by Fireworks (429). "
                        "Retrying in %ds (attempt %d/%d).",
                        delay,
                        attempt,
                        _MAX_RETRIES,
                    )
                    time.sleep(delay)
                    continue

                if status >= 500:
                    # Server error — retry.
                    delay = _RETRY_BASE_DELAY_SECONDS * attempt
                    logger.warning(
                        "Fireworks server error (HTTP %d). "
                        "Retrying in %ds (attempt %d/%d).",
                        status,
                        delay,
                        attempt,
                        _MAX_RETRIES,
                    )
                    time.sleep(delay)
                    continue

                # Other client errors — do not retry.
                raise ProviderError(
                    f"Fireworks API error (HTTP {status}) for model "
                    f"'{model_id}': {body}"
                ) from exc

            except APITimeoutError as exc:
                last_error = exc
                delay = _RETRY_BASE_DELAY_SECONDS * attempt
                logger.warning(
                    "Fireworks request timed out. "
                    "Retrying in %ds (attempt %d/%d).",
                    delay,
                    attempt,
                    _MAX_RETRIES,
                )
                time.sleep(delay)

            except APIConnectionError as exc:
                last_error = exc
                delay = _RETRY_BASE_DELAY_SECONDS * attempt
                logger.warning(
                    "Fireworks connection error. "
                    "Retrying in %ds (attempt %d/%d).",
                    delay,
                    attempt,
                    _MAX_RETRIES,
                )
                time.sleep(delay)

            except Exception as exc:
                # Unexpected error — surface immediately.
                raise ProviderError(
                    f"Unexpected error during Fireworks inference "
                    f"(model={model_id}): {exc}"
                ) from exc

        # All retries exhausted.
        raise ProviderError(
            f"Fireworks inference failed after {_MAX_RETRIES} attempts "
            f"for model '{model_id}'. Last error: {last_error}"
        )
