"""
Video validation — verify format, duration, and extract metadata via FFprobe.

Validates that a video file meets DescribeX requirements before entering
the caption pipeline.  Returns a :class:`VideoInfo` dataclass on success.
"""

from __future__ import annotations

import json
import os
import subprocess
from dataclasses import dataclass

from engine.utils.config import EngineConfig
from engine.utils.exceptions import PreprocessingError, ValidationError
from engine.utils.logging import get_logger

logger = get_logger(__name__)

# Formats accepted by the preprocessing pipeline.
SUPPORTED_FORMATS: tuple[str, ...] = (".mp4", ".mov", ".avi", ".webm", ".mkv")


@dataclass(frozen=True)
class VideoInfo:
    """Metadata extracted from a validated video file."""

    duration_seconds: float
    width: int
    height: int
    fps: float
    codec: str


def _probe_video(video_path: str) -> dict:
    """Run FFprobe and return the parsed JSON output.

    Raises:
        PreprocessingError: If FFprobe is not found or returns a non-zero exit
            code.
    """
    cmd = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=duration,width,height,r_frame_rate,codec_name",
        "-show_entries", "format=duration",
        "-of", "json",
        video_path,
    ]

    logger.debug("Running FFprobe: %s", " ".join(cmd))

    try:
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:
        raise PreprocessingError(
            "FFprobe not found. Ensure FFmpeg is installed and on PATH."
        ) from exc
    except subprocess.CalledProcessError as exc:
        raise PreprocessingError(
            f"FFprobe failed (exit {exc.returncode}): {exc.stderr.strip()}"
        ) from exc

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise PreprocessingError(
            "FFprobe returned invalid JSON output."
        ) from exc


def _parse_fps(r_frame_rate: str) -> float:
    """Parse the ``r_frame_rate`` fraction string (e.g. ``'30/1'``)."""
    numerator, _, denominator = r_frame_rate.partition("/")
    if denominator and float(denominator) != 0:
        return float(numerator) / float(denominator)
    return float(numerator)


def _extract_duration(probe_data: dict) -> float:
    """Return the video duration in seconds.

    Prefers the stream-level duration; falls back to the format-level
    duration when the stream value is missing or invalid.

    Raises:
        PreprocessingError: If no valid duration is found.
    """
    # Try stream duration first.
    streams = probe_data.get("streams", [])
    if streams:
        raw = streams[0].get("duration")
        if raw is not None:
            try:
                return float(raw)
            except (ValueError, TypeError):
                pass

    # Fall back to format duration.
    raw = probe_data.get("format", {}).get("duration")
    if raw is not None:
        try:
            return float(raw)
        except (ValueError, TypeError):
            pass

    raise PreprocessingError(
        "Could not determine video duration from FFprobe output."
    )


def validate_video(video_path: str, config: EngineConfig) -> VideoInfo:
    """Validate a video file and extract its metadata.

    The function performs the following checks in order:

    1. File exists on disk.
    2. File extension is in :data:`SUPPORTED_FORMATS`.
    3. File is non-empty.
    4. FFprobe can read the file and extract valid metadata.
    5. Duration does not exceed ``config.max_video_duration_seconds``.

    Args:
        video_path: Absolute or relative path to the video file.
        config: Engine configuration with validation thresholds.

    Returns:
        A :class:`VideoInfo` instance containing the extracted metadata.

    Raises:
        PreprocessingError: If the file does not exist or FFprobe fails.
        ValidationError: If the video fails a validation check.
    """
    logger.info("Validating video: %s", video_path)

    # 1. Existence check.
    if not os.path.isfile(video_path):
        raise PreprocessingError(f"Video file not found: {video_path}")

    # 2. Extension check.
    _, ext = os.path.splitext(video_path)
    if ext.lower() not in SUPPORTED_FORMATS:
        raise ValidationError(
            f"Unsupported video format '{ext}'. "
            f"Accepted formats: {', '.join(SUPPORTED_FORMATS)}"
        )
    logger.debug("File extension '%s' is supported.", ext)

    # 3. Non-empty check.
    if os.path.getsize(video_path) == 0:
        raise ValidationError("Video file is empty (0 bytes).")
    logger.debug("File is non-empty.")

    # 4. Probe metadata.
    probe_data = _probe_video(video_path)

    streams = probe_data.get("streams", [])
    if not streams:
        raise PreprocessingError(
            "FFprobe found no video streams in the file."
        )

    stream = streams[0]
    duration = _extract_duration(probe_data)
    width: int = int(stream["width"])
    height: int = int(stream["height"])
    fps = _parse_fps(stream.get("r_frame_rate", "30/1"))
    codec: str = stream.get("codec_name", "unknown")

    logger.info(
        "Probed metadata — duration=%.2fs, resolution=%dx%d, fps=%.2f, codec=%s",
        duration, width, height, fps, codec,
    )

    # 5. Duration limit.
    if duration > config.max_video_duration_seconds:
        raise ValidationError(
            f"Video duration ({duration:.1f}s) exceeds the maximum "
            f"allowed ({config.max_video_duration_seconds}s)."
        )
    logger.info("Video validation passed.")

    return VideoInfo(
        duration_seconds=duration,
        width=width,
        height=height,
        fps=fps,
        codec=codec,
    )
