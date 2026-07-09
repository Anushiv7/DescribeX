"""
Prompt template loader.

Reads plain-text prompt templates from the ``templates/`` directory
adjacent to this module. Templates use Python ``str.format`` placeholders
(e.g. ``{frame_count}``) that are filled in at build time.
"""

from __future__ import annotations

import os

from engine.utils.logging import get_logger

logger = get_logger(__name__)

_TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")


def load_template(template_name: str) -> str:
    """Load a prompt template file by name.

    Args:
        template_name: The filename of the template (e.g.,
            ``'scene_description.txt'``).

    Returns:
        The template string with placeholders intact.

    Raises:
        FileNotFoundError: If the template does not exist.
    """
    template_path = os.path.join(_TEMPLATES_DIR, template_name)

    if not os.path.isfile(template_path):
        raise FileNotFoundError(f"Prompt template not found: {template_path}")

    with open(template_path, "r", encoding="utf-8") as f:
        content = f.read()

    logger.debug("Loaded template: %s (%d chars)", template_name, len(content))
    return content
