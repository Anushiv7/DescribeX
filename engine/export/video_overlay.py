"""
Video overlay module.

Burns caption text onto a video file using FFmpeg's drawtext filter.
Requires FFmpeg to be installed and available on the system PATH.
"""

from __future__ import annotations

import json
import os
import platform
import subprocess
import textwrap

from engine.utils.exceptions import ExportError
from engine.utils.logging import get_logger

logger = get_logger(__name__)

# Vertical position presets for the drawtext filter.
_POSITION_MAP: dict[str, str] = {
    "bottom": "y=h-th-60",
    "top": "y=60",
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


def _get_video_width(video_path: str) -> int:
    """Extract video width using ffprobe."""
    try:
        cmd = [
            "ffprobe", "-v", "error", "-select_streams", "v:0",
            "-show_entries", "stream=width", "-of", "json", video_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        return int(data["streams"][0]["width"])
    except Exception:
        return 1280  # Reasonable fallback if extraction fails


def _wrap_and_fit_text(text: str, video_width: int, max_lines: int = 3, base_font_size: int = 24) -> tuple[str, int]:
    """Wrap text to fit within the video width and reduce font size if necessary."""
    # Normalize whitespace to avoid awkward wraps on existing newlines/spaces
    text = " ".join(text.split())
    
    font_size = base_font_size
    min_font_size = 12
    wrapped_lines = []
    
    while font_size >= min_font_size:
        # Approximate character width based on font size (0.6 is a standard average for sans-serif)
        char_width = max(1, int(0.6 * font_size))
        # 90% of video width provides a safe margin on both left and right to prevent overflowing
        safe_width = int(video_width * 0.9)
        chars_per_line = max(10, safe_width // char_width)
        
        # Break text into multiple lines, preserving whole words
        wrapped_lines = textwrap.wrap(text, width=chars_per_line, break_long_words=False)
        
        # If it fits within our line limit, we're done
        if len(wrapped_lines) <= max_lines:
            break
            
        font_size -= 2
        
    # Join with newlines for FFmpeg drawtext
    return "\n".join(wrapped_lines), font_size


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

    video_width = _get_video_width(video_path)
    wrapped_text, adjusted_font_size = _wrap_and_fit_text(
        caption_text, 
        video_width, 
        max_lines=3, 
        base_font_size=font_size
    )

    escaped_text = _escape_for_drawtext(wrapped_text)

    drawtext_filter = (
        f"drawtext=text='{escaped_text}'"
        f":fontsize={adjusted_font_size}"
        f":fontcolor={font_color}"
        f":box=1"
        f":boxcolor={bg_color}"
        f":boxborderw=10"
        f":x=(w-tw)/2"
        f":{y_expr}"
    )

    if platform.system() == "Windows":
        for font_path in ["C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/segoeui.ttf"]:
            if os.path.exists(font_path):
                # Escape the colon in the drive letter (e.g., C\:/...) for FFmpeg filter syntax
                escaped_font_path = font_path.replace(":", "\\:")
                drawtext_filter += f":fontfile='{escaped_font_path}'"
                break

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
