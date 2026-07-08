"""
Centralized configuration for the DescribeX caption engine.

All runtime settings are defined here and loaded from environment
variables. No hardcoded values should be scattered through the codebase.

Usage:
    from engine.utils.config import get_config

    config = get_config()
    print(config.max_video_duration_seconds)
"""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class EngineConfig(BaseSettings):
    """Runtime configuration for the caption engine.

    Values are loaded from environment variables prefixed with ``DESCRIBEX_``.
    A ``.env`` file in the project root is also supported.

    Attributes:
        fireworks_api_key: API key for the Fireworks AI provider.
        model_id: Identifier of the AI model to use for inference.
        max_video_duration_seconds: Maximum allowed video length in seconds.
        max_frames: Maximum number of frames to sample from a video.
        temperature: Sampling temperature for caption generation.
        output_format: Output serialization format.
        log_level: Logging verbosity level.
        request_timeout_seconds: Timeout for external API requests.
    """

    model_config = SettingsConfigDict(
        env_prefix="DESCRIBEX_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- AI Provider ---
    fireworks_api_key: str = Field(
        default="",
        description="API key for the Fireworks AI provider.",
    )
    model_id: str = Field(
        default="",
        description="Identifier of the AI model to use for inference.",
    )

    # --- Preprocessing Limits ---
    max_video_duration_seconds: int = Field(
        default=120,
        description="Maximum allowed video duration in seconds.",
    )
    max_frames: int = Field(
        default=60,
        description="Maximum number of representative frames to sample.",
    )

    # --- Inference ---
    temperature: float = Field(
        default=0.3,
        description="Sampling temperature for text generation.",
    )

    # --- Output ---
    output_format: str = Field(
        default="json",
        description="Output serialization format.",
    )

    # --- Runtime ---
    log_level: str = Field(
        default="INFO",
        description="Logging verbosity (DEBUG, INFO, WARNING, ERROR, CRITICAL).",
    )
    request_timeout_seconds: int = Field(
        default=60,
        description="Timeout in seconds for external API requests.",
    )


@lru_cache(maxsize=1)
def get_config() -> EngineConfig:
    """Return a singleton ``EngineConfig`` instance.

    The config is created once and cached for the lifetime of the process.
    """
    return EngineConfig()
