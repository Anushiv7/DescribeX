"""
Caption formatting and validation module.

Parses raw AI model responses (expected JSON) into a validated
caption dictionary with all required style keys present and cleaned.
"""

from __future__ import annotations

import json
import re

from engine.utils.exceptions import FormattingError
from engine.utils.logging import get_logger

logger = get_logger(__name__)

REQUIRED_STYLES: frozenset[str] = frozenset(
    {"formal", "sarcastic", "humorous_tech", "humorous_non_tech"}
)


def _strip_code_fences(text: str) -> str:
    """Remove markdown code fences (```json ... ``` or ``` ... ```) if present."""
    # Match ```json ... ``` or ``` ... ``` (with optional language tag)
    pattern = r"^```(?:json)?\s*\n?(.*?)\n?\s*```$"
    match = re.search(pattern, text.strip(), re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()


def _extract_json_object(text: str) -> str:
    """Extract the first plausible JSON object from a string.

    Finds content between the first '{' and the last '}' in *text*.

    Raises:
        FormattingError: If no JSON object boundaries are found.
    """
    first_brace = text.find("{")
    last_brace = text.rfind("}")
    if first_brace == -1 or last_brace == -1 or last_brace <= first_brace:
        raise FormattingError(
            "No JSON object found in AI response. "
            "Expected a JSON object with caption styles."
        )
    return text[first_brace : last_brace + 1]


def _clean_caption(value: str) -> str:
    """Strip whitespace and remove surrounding double quotes from a caption."""
    cleaned = value.strip()
    # Remove surrounding double-quotes if the entire string is quoted
    if len(cleaned) >= 2 and cleaned.startswith('"') and cleaned.endswith('"'):
        cleaned = cleaned[1:-1].strip()
    return cleaned


def format_captions(raw_response: str) -> dict[str, str]:
    """Parse and validate the raw AI response into a caption dictionary.

    Args:
        raw_response: The raw string response from the AI model,
            expected to be a JSON object.

    Returns:
        A validated dict mapping style names to caption strings.

    Raises:
        FormattingError: If the response cannot be parsed or is missing styles.
    """
    if not raw_response or not raw_response.strip():
        raise FormattingError("Empty response from AI model.")

    text = _strip_code_fences(raw_response)

    # Attempt direct JSON parse first
    parsed: dict[str, str] | None = None
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        # Fallback: try to extract a JSON object from the text
        logger.debug("Direct JSON parse failed; attempting extraction.")
        try:
            extracted = _extract_json_object(text)
            parsed = json.loads(extracted)
        except json.JSONDecodeError as exc:
            raise FormattingError(
                f"Failed to parse AI response as JSON: {exc}"
            ) from exc

    if not isinstance(parsed, dict):
        raise FormattingError(
            f"Expected a JSON object, got {type(parsed).__name__}."
        )

    # Validate required style keys
    missing = REQUIRED_STYLES - parsed.keys()
    if missing:
        raise FormattingError(
            f"AI response missing required caption styles: {sorted(missing)}"
        )

    # Clean and validate each caption value
    result: dict[str, str] = {}
    for style in REQUIRED_STYLES:
        raw_value = parsed[style]
        if not isinstance(raw_value, str):
            raise FormattingError(
                f"Caption for style '{style}' must be a string, "
                f"got {type(raw_value).__name__}."
            )
        cleaned = _clean_caption(raw_value)
        if not cleaned:
            raise FormattingError(
                f"Caption for style '{style}' is empty after cleanup."
            )
        result[style] = cleaned

    logger.info(
        "Formatted %d caption style(s) successfully.", len(result)
    )
    return result
