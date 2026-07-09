"""
Abstract base class for AI providers.

The CaptionEngine communicates exclusively through this interface.
It never knows whether Fireworks, Gemini, or any other provider is
being used.  New providers are added by subclassing ``BaseProvider``
and registering them in the provider factory.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class BaseProvider(ABC):
    """Provider-agnostic interface for AI inference.

    Every concrete provider (Fireworks, Gemini, future providers) must
    implement the two abstract methods below.  The rest of the engine
    calls only these methods, keeping provider details fully isolated.
    """

    # ------------------------------------------------------------------
    # Abstract interface
    # ------------------------------------------------------------------

    @abstractmethod
    def generate_scene_description(
        self,
        messages: list[dict],
    ) -> str:
        """Send a multimodal (vision) prompt and return the scene description.

        Args:
            messages: A list of message dicts in OpenAI chat-completions
                format.  The user message contains interleaved text and
                base64-encoded image payloads.

        Returns:
            The model's textual scene description.

        Raises:
            ProviderError: On authentication failure, timeout, model
                unavailability, or any other provider-level error.
        """

    @abstractmethod
    def generate_captions(
        self,
        messages: list[dict],
    ) -> str:
        """Send a text prompt and return the raw caption JSON string.

        Args:
            messages: A list of message dicts (text-only) requesting
                multi-style caption generation.

        Returns:
            The raw response string from the model — expected to be
            a JSON object, but the caller is responsible for parsing.

        Raises:
            ProviderError: On authentication failure, timeout, model
                unavailability, or any other provider-level error.
        """
