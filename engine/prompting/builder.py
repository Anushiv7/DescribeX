"""
Frame extraction — decode video into individual JPEG frames via FFmpeg.

Calculates an extraction frame rate that keeps the total number of frames
within the configured budget, then shells out to FFmpeg.
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

from engine.preprocessing.validator import VideoInfo
from engine.utils.exceptions import PreprocessingError
from engine.utils.logging import get_logger

logger = get_logger(__name__)


def extract_frames(
    video_path: str,
    output_dir: str,
    video_info: VideoInfo,
    max_frames: int = 60,
) -> list[str]:
    """Extract JPEG frames from a video file.

    The extraction frame rate is calculated so that the total number of
    extracted frames stays within *max_frames*.  If the calculated rate
    exceeds the video's native fps, the native fps is used instead (i.e.
    we never up-sample).

    Args:
        video_path: Path to the source video file.
        output_dir: Directory where extracted frames will be written.
            Created automatically if it does not exist.
        video_info: Metadata returned by :func:`validate_video`.
        max_frames: Upper bound on the number of frames to extract.

    Returns:
        Sorted list of absolute paths to the extracted JPEG frames.

    Raises:
        PreprocessingError: If FFmpeg fails or no frames are produced.
    """
    os.makedirs(output_dir, exist_ok=True)

    # --- Determine extraction fps ---
    extraction_fps = max_frames / video_info.duration_seconds
    # Never exceed the video's native fps.
    if extraction_fps > video_info.fps:
        extraction_fps = video_info.fps

    logger.info(
        "Extracting frames — target fps=%.4f (native=%.2f, budget=%d, duration=%.2fs)",
        extraction_fps,
        video_info.fps,
        max_frames,
        video_info.duration_seconds,
    )

    output_pattern = os.path.join(output_dir, "frame_%05d.jpg")

    # Cap frame width at 640px. Vision models downscale large images
    # internally anyway, so this costs no caption quality while cutting
    # per-frame memory (and the base64 payload built from it later) by
    # roughly 10x for typical 1080p+ source videos — the main fix for
    # OOM crashes on memory-constrained free hosting tiers.
    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-vf", f"fps={extraction_fps},scale='min(640,iw)':-2",
        "-q:v", "2",
        output_pattern,
    ]

    logger.debug("Running FFmpeg: %s", " ".join(cmd))

    try:
        subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:
        raise PreprocessingError(
            "FFmpeg not found. Ensure FFmpeg is installed and on PATH."
        ) from exc
    except subprocess.CalledProcessError as exc:
        raise PreprocessingError(
            f"FFmpeg frame extraction failed (exit {exc.returncode}): "
            f"{exc.stderr.strip()}"
        ) from exc

    # --- Collect extracted frame paths ---
    frame_paths = sorted(
        str(p) for p in Path(output_dir).glob("frame_*.jpg")
    )

    if not frame_paths:
        raise PreprocessingError(
            "FFmpeg completed but no frames were produced."
        )

    logger.info("Extracted %d frames to %s", len(frame_paths), output_dir)
    return frame_paths
