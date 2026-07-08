"""
CaptionEngine — Main orchestrator for the DescribeX caption pipeline.

The engine processes a video through seven sequential stages:

    1. Video Validation
    2. Frame Extraction  (FFmpeg)
    3. Smart Frame Sampling
    4. Canonical Prompt Construction
    5. Canonical Scene Description  (AI vision model)
    6. Multi-style Caption Generation  (AI text model)
    7. Caption Formatting

The engine analyzes a video **once** and produces captions in every
supported style from that single analysis.  This reduces latency,
API cost, and ensures stylistic consistency across outputs.

Usage:
    from engine.core.caption_engine import CaptionEngine

    engine = CaptionEngine()
    captions = engine.generate_captions("/path/to/video.mp4")
"""

from __future__ import annotations

from engine.utils.config import EngineConfig, get_config
from engine.utils.logging import get_logger


class CaptionEngine:
    """Orchestrates the full caption generation pipeline.

    The public interface is intentionally minimal:

    * Construct with an optional :class:`EngineConfig`.
    * Call :meth:`generate_captions` with a video path.
    * Receive a ``dict`` mapping style names to caption strings.

    All internal pipeline stages (validation, extraction, sampling,
    prompting, inference, formatting) are coordinated behind this
    single entry point.
    """

    def __init__(self, config: EngineConfig | None = None) -> None:
        """Initialise the CaptionEngine.

        Args:
            config: Optional runtime configuration.  When *None* the
                shared singleton from :func:`get_config` is used.
        """
        self._config = config or get_config()
        self._logger = get_logger(__name__)
        self._logger.info("CaptionEngine initialized.")

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def config(self) -> EngineConfig:
        """The runtime configuration backing this engine instance."""
        return self._config

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate_captions(self, video_path: str) -> dict[str, str]:
        """Generate captions in all supported styles for a video.

        The engine analyses the video **once** to build a canonical
        scene description, then derives every supported caption style
        from that shared understanding.

        Args:
            video_path: Path to the input video file.

        Returns:
            A dictionary mapping each style name (e.g. ``"formal"``,
            ``"sarcastic"``) to its generated caption string.

        Raises:
            NotImplementedError: The pipeline stages are not yet
                implemented (Phase 1 placeholder).
        """
        self._logger.info("generate_captions called for: %s", video_path)
        raise NotImplementedError(
            "Caption generation pipeline is not yet implemented. "
            "Pipeline stages will be wired in subsequent phases."
        )
