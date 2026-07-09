"""
Google Gemini provider implementation.

Uses the ``google-genai`` SDK to communicate with the Gemini API.
Model IDs are read exclusively from :class:`EngineConfig` — never hardcoded.

The provider translates the engine's OpenAI-format messages into the
Gemini-native format internally, so the rest of the engine remains
completely provider-agnostic.
"""

from __future__ import annotations

import time

from engine.providers.base import BaseProvider
from engine.utils.config import EngineConfig, get_config
from engine.utils.exceptions import ProviderError
from engine.utils.logging import get_logger

logger = get_logger(__name__)

# Retry parameters.
_MAX_RETRIES = 3
_RETRY_BASE_DELAY_SECONDS = 2


class GeminiProvider(BaseProvider):
    """Google Gemini provider using the google-genai SDK."""

    def __init__(self, config: EngineConfig | None = None) -> None:
        self._config = config or get_config()

        if not self._config.gemini_api_key:
            raise ProviderError(
                "Gemini API key is not configured. "
                "Set DESCRIBEX_GEMINI_API_KEY in your environment or .env file."
            )

        try:
            from google import genai  # type: ignore[import-untyped]

            self._client = genai.Client(api_key=self._config.gemini_api_key)
        except ImportError as exc:
            raise ProviderError(
                "The 'google-genai' package is required for the Gemini provider. "
                "Install it with: pip install google-genai"
            ) from exc

        logger.info("GeminiProvider initialized.")

    # ------------------------------------------------------------------
    # Public interface (implements BaseProvider)
    # ------------------------------------------------------------------

    def generate_scene_description(self, messages: list[dict]) -> str:
        """Send a vision prompt to Gemini and return the scene description."""
        model_id = self._config.vision_model_id
        logger.info(
            "Generating scene description via Gemini (model=%s)", model_id
        )
        contents = self._convert_messages(messages)
        return self._call(model_id, contents)

    def generate_captions(self, messages: list[dict]) -> str:
        """Send a text prompt to Gemini and return raw caption JSON."""
        model_id = self._config.text_model_id
        logger.info("Generating captions via Gemini (model=%s)", model_id)
        contents = self._convert_messages(messages)
        return self._call(model_id, contents)

    # ------------------------------------------------------------------
    # Message format conversion
    # ------------------------------------------------------------------

    @staticmethod
    def _convert_messages(messages: list[dict]) -> list:
        """Convert OpenAI-format messages to Gemini-native content parts.

        The engine builds prompts in OpenAI chat-completions format.
        This method translates them for the Gemini SDK.

        Handles both simple string content and multimodal content arrays
        (text + image_url with base64 data URIs).
        """
        from google.genai import types  # type: ignore[import-untyped]
        import base64

        parts: list = []

        for msg in messages:
            content = msg.get("content", "")

            if isinstance(content, str):
                # Simple text message.
                parts.append(types.Part.from_text(text=content))
                continue

            if isinstance(content, list):
                # Multimodal content array.
                for item in content:
                    item_type = item.get("type", "")

                    if item_type == "text":
                        parts.append(
                            types.Part.from_text(text=item.get("text", ""))
                        )

                    elif item_type == "image_url":
                        image_url = item.get("image_url", {}).get("url", "")
                        if image_url.startswith("data:"):
                            # Parse base64 data URI.
                            # Format: data:<mime>;base64,<data>
                            header, _, b64_data = image_url.partition(",")
                            mime_type = header.split(";")[0].replace(
                                "data:", ""
                            )
                            image_bytes = base64.b64decode(b64_data)
                            parts.append(
                                types.Part.from_bytes(
                                    data=image_bytes,
                                    mime_type=mime_type or "image/jpeg",
                                )
                            )
                        else:
                            # URL-based image — pass as file URI.
                            parts.append(
                                types.Part.from_uri(
                                    file_uri=image_url,
                                    mime_type="image/jpeg",
                                )
                            )

        return [types.Content(role="user", parts=parts)]

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _call(self, model_id: str, contents: list) -> str:
        """Execute a Gemini generate_content request with retry logic.

        Raises:
            ProviderError: On any unrecoverable failure including model
                unavailability, auth failures, or exhausted retries.
        """
        from google.genai import types  # type: ignore[import-untyped]

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
                    "Gemini API call attempt %d/%d (model=%s)",
                    attempt,
                    _MAX_RETRIES,
                    model_id,
                )
                response = self._client.models.generate_content(
                    model=model_id,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        temperature=self._config.temperature,
                    ),
                )

                if not response.text:
                    raise ProviderError(
                        f"Gemini returned an empty response for model {model_id}."
                    )

                logger.info("Gemini API call succeeded (model=%s).", model_id)
                return response.text

            except ProviderError:
                # Re-raise our own errors immediately.
                raise

            except Exception as exc:
                last_error = exc
                error_msg = str(exc).lower()

                # Check for non-retryable errors.
                if any(
                    keyword in error_msg
                    for keyword in ("not found", "404", "invalid", "permission")
                ):
                    raise ProviderError(
                        f"Gemini error for model '{model_id}': {exc}. "
                        f"Verify the model ID is correct and your API key "
                        f"has the required permissions."
                    ) from exc

                # Retryable error — back off.
                delay = _RETRY_BASE_DELAY_SECONDS * attempt
                logger.warning(
                    "Gemini error: %s. Retrying in %ds (attempt %d/%d).",
                    exc,
                    delay,
                    attempt,
                    _MAX_RETRIES,
                )
                time.sleep(delay)

        # All retries exhausted.
        raise ProviderError(
            f"Gemini inference failed after {_MAX_RETRIES} attempts "
            f"for model '{model_id}'. Last error: {last_error}"
        )
