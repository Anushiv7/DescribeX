"""
TXT export module.

Writes captions to a human-readable plain-text file with
section headers for each style.
"""

from __future__ import annotations

import os

from engine.utils.exceptions import ExportError
from engine.utils.logging import get_logger

logger = get_logger(__name__)

# Ordered mapping so the output file has a consistent, readable structure.
_STYLE_DISPLAY_NAMES: dict[str, str] = {
    "formal": "Formal",
    "sarcastic": "Sarcastic",
    "humorous_tech": "Humorous (Tech)",
    "humorous_non_tech": "Humorous (Non-Tech)",
}


def export_txt(captions: dict[str, str], output_path: str) -> str:
    """Export captions to a formatted TXT file.

    Args:
        captions: A dict mapping style names to caption strings.
        output_path: Path to write the TXT file.

    Returns:
        The absolute path to the written file.

    Raises:
        ExportError: If writing fails.
    """
    try:
        abs_path = os.path.abspath(output_path)
        os.makedirs(os.path.dirname(abs_path) or ".", exist_ok=True)

        with open(abs_path, "w", encoding="utf-8") as fh:
            fh.write("DescribeX — Generated Captions\n")
            fh.write("=" * 40 + "\n\n")

            for style_key, display_name in _STYLE_DISPLAY_NAMES.items():
                caption_text = captions.get(style_key, "")
                fh.write(f"{display_name}\n")
                fh.write("-" * len(display_name) + "\n")
                fh.write(f"{caption_text}\n\n")

        logger.info("Exported captions to TXT: %s", abs_path)
        return abs_path

    except OSError as exc:
        raise ExportError(
            f"Failed to write TXT export to '{output_path}': {exc}"
        ) from exc
