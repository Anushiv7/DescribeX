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

import tempfile
from contextlib import contextmanager
from typing import Iterator

from engine.formatting import format_captions
from engine.preprocessing import (
    extract_frames,
    sample_frames,
    validate_video,
)
from engine.prompting import build_scene_prompt, build_style_prompt
from engine.providers import create_provider
from engine.utils.config import EngineConfig, get_config
from engine.utils.logging import get_logger


@contextmanager
def temp_frame_dir() -> Iterator[str]:
    """Context manager for a temporary frame extraction directory."""
    temp_dir = tempfile.mkdtemp(prefix="describex_frames_")
    try:
        yield temp_dir
    finally:
        import shutil

        shutil.rmtree(temp_dir, ignore_errors=True)


class CaptionEngine:
    """Orchestrates the full caption generation pipeline."""

    def __init__(self, config: EngineConfig | None = None) -> None:
        """Initialise the CaptionEngine.

        Args:
            config: Optional runtime configuration.  When *None* the
                shared singleton from :func:`get_config` is used.
        """
        self._config = config or get_config()
        self._logger = get_logger(__name__)
        # Initialize the provider factory here.
        self._provider = create_provider(self._config)
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
        """
        self._logger.info("Starting caption pipeline for: %s", video_path)

        # Stage 1: Validate video
        self._logger.info("Stage 1: Video Validation")
        video_info = validate_video(video_path, self._config)

        with temp_frame_dir() as frame_dir:
            # Stage 2: Extract frames
            self._logger.info("Stage 2: Frame Extraction")
            all_frames = extract_frames(
                video_path, frame_dir, video_info, self._config.max_frames
            )

            # Stage 3: Smart sample
            self._logger.info("Stage 3: Smart Sampling")
            sampled_frames = sample_frames(
                all_frames, self._config.target_sample_frames
            )

            # Stage 4: Canonical Prompt Construction
            self._logger.info("Stage 4: Prompt Construction")
            vision_messages = build_scene_prompt(sampled_frames)

            # Stage 5: Canonical Scene Description
            self._logger.info("Stage 5: Scene Description (Vision Inference)")
            scene_description = self._provider.generate_scene_description(
                vision_messages
            )

            # Stage 6: Multi-style Caption Generation
            self._logger.info("Stage 6: Caption Generation (Text Inference)")
            style_messages = build_style_prompt(scene_description)
            raw_captions = self._provider.generate_captions(style_messages)

            # Stage 7: Formatting
            self._logger.info("Stage 7: Caption Formatting")
            captions = format_captions(raw_captions)

            self._logger.info("Caption pipeline completed successfully.")
            return captions
