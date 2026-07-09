"""
Video overlay module.

Burns caption text onto a video file using FFmpeg's drawtext filter.
Requires FFmpeg to be installed and available on the system PATH.
"""

from __future__ import annotations

import os
import subprocess

from engine.utils.exceptions import ExportError
from engine.utils.logging import get_logger

logger = get_logger(__name__)

# Vertical position presets for the drawtext filter.
_POSITION_MAP: dict[str, str] = {
    "bottom": "y=h-th-40",
    "top": "y=40",
    "center": "y=(h-th)/2",
}


def _escape_for_drawtext(text: str) -> str:
    """Escape special characters for the FFmpeg drawtext filter.

    FFmpeg drawtext requires backslash-escaping of single quotes,
    colons, and backslashes themselves.
    """
    # Order matters: escape backslashes first to avoid double-escaping
    text = text.replace("\\", "\\\\")
    text = text.replace("'", "\\'")
    text = text.replace(":", "\\:")
    return text


def burn_captions(
    video_path: str,
    caption_text: str,
    output_path: str,
    font_size: int = 24,
    font_color: str = "white",
    bg_color: str = "black@0.7",
    position: str = "bottom",
) -> str:
    """Burn caption text onto a video using FFmpeg drawtext filter.

    Args:
        video_path: Path to the input video.
        caption_text: The caption text to overlay.
        output_path: Path for the output video.
        font_size: Font size for the caption text.
        font_color: Font color.
        bg_color: Background color/opacity for the text box.
        position: Position of the text ('bottom', 'top', 'center').

    Returns:
        The absolute path to the output video.

    Raises:
        ExportError: If FFmpeg fails or an invalid position is given.
    """
    y_expr = _POSITION_MAP.get(position)
    if y_expr is None:
        raise ExportError(
            f"Invalid position '{position}'. "
            f"Must be one of: {sorted(_POSITION_MAP.keys())}"
        )

    abs_output = os.path.abspath(output_path)
    os.makedirs(os.path.dirname(abs_output) or ".", exist_ok=True)

    escaped_text = _escape_for_drawtext(caption_text)

    drawtext_filter = (
        f"drawtext=text='{escaped_text}'"
        f":fontsize={font_size}"
        f":fontcolor={font_color}"
        f":box=1"
        f":boxcolor={bg_color}"
        f":boxborderw=10"
        f":x=(w-tw)/2"
        f":{y_expr}"
    )

    cmd = [
        "ffmpeg",
        "-i", video_path,
        "-vf", drawtext_filter,
        "-codec:a", "copy",
        "-y",
        abs_output,
    ]

    logger.info(
        "Burning captions onto video: %s -> %s", video_path, abs_output
    )

    try:
        subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:
        raise ExportError(
            "FFmpeg not found. Ensure FFmpeg is installed and on the system PATH."
        ) from exc
    except subprocess.CalledProcessError as exc:
        raise ExportError(
            f"FFmpeg failed (exit code {exc.returncode}): {exc.stderr}"
        ) from exc

    logger.info("Video with burned captions saved to: %s", abs_output)
    return abs_output
