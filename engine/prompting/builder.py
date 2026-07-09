"""
Prompt builder — constructs ready-to-send prompt messages.

Two public entry points:

* :func:`build_scene_prompt` — multimodal prompt with base64-encoded
  frames for the canonical scene-description step.
* :func:`build_style_prompt` — text-only prompt that turns a scene
  description into multi-style captions.

Both return messages in the OpenAI chat-completions format so the
provider layer can forward them without transformation.
"""

from __future__ import annotations

import base64
from typing import Any

from engine.prompting.loader import load_template
from engine.utils.logging import get_logger

logger = get_logger(__name__)

# ---------------------------------------------------------------------------
# Template filenames (co-located in templates/)
# ---------------------------------------------------------------------------
_SCENE_TEMPLATE = "scene_description.txt"
_STYLE_TEMPLATE = "caption_styles.txt"


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def build_scene_prompt(frame_paths: list[str]) -> list[dict[str, Any]]:
    """Build a multimodal prompt for canonical scene description.

    Loads the scene-description template, injects the frame count, and
    attaches every sampled frame as a base64-encoded JPEG image.

    Args:
        frame_paths: Absolute paths to the sampled frame images.

    Returns:
        A messages list in OpenAI chat-completions format containing a
        single ``user`` message whose ``content`` is a list of text and
        image_url parts.

    Raises:
        FileNotFoundError: If a frame path does not exist.
    """
    template = load_template(_SCENE_TEMPLATE)
    prompt_text = template.format(frame_count=len(frame_paths))

    # Build the content parts list: leading text + one image per frame
    content_parts: list[dict[str, Any]] = [
        {"type": "text", "text": prompt_text},
    ]

    for path in frame_paths:
        encoded = _encode_image(path)
        content_parts.append(
            {
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{encoded}"},
            }
        )

    messages: list[dict[str, Any]] = [
        {"role": "user", "content": content_parts},
    ]

    logger.info(
        "Built scene prompt with %d frame(s) attached",
        len(frame_paths),
    )
    return messages


def build_style_prompt(scene_description: str) -> list[dict[str, Any]]:
    """Build a text prompt for multi-style caption generation.

    Loads the caption-styles template and injects the scene description
    produced by the previous pipeline stage.

    Args:
        scene_description: The canonical scene description text.

    Returns:
        A messages list in OpenAI chat-completions format containing a
        single ``user`` message with the formatted prompt as a string.
    """
    template = load_template(_STYLE_TEMPLATE)
    prompt_text = template.format(scene_description=scene_description)

    messages: list[dict[str, Any]] = [
        {"role": "user", "content": prompt_text},
    ]

    logger.info("Built style prompt from scene description")
    return messages


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _encode_image(path: str) -> str:
    """Read an image file and return its base64 representation.

    Args:
        path: Absolute path to the image file.

    Returns:
        A base64-encoded string of the file contents.

    Raises:
        FileNotFoundError: If *path* does not point to an existing file.
    """
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")
