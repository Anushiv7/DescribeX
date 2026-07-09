"""
Smart frame sampling — select a representative subset of extracted frames.

Uses uniform interval sampling to reduce the frame set to a target count
while preserving temporal coverage.
"""

from __future__ import annotations

from engine.utils.logging import get_logger

logger = get_logger(__name__)


def sample_frames(
    frame_paths: list[str],
    target_count: int = 50,
) -> list[str]:
    """Select a uniformly-spaced subset of frames.

    If the number of available frames is already at or below
    *target_count*, all frames are returned as-is.  Otherwise, frames
    are picked at uniform intervals with the first and last frame always
    included.

    Args:
        frame_paths: Sorted list of frame file paths.
        target_count: Desired number of frames in the output.

    Returns:
        A list of selected frame paths in their original order.
    """
    total = len(frame_paths)

    if total <= target_count:
        logger.info(
            "Frame count (%d) within target (%d) — keeping all frames.",
            total,
            target_count,
        )
        return list(frame_paths)

    # Uniform interval sampling.
    step = total / target_count
    indices: list[int] = [int(i * step) for i in range(target_count)]

    # Guarantee the first and last frame are included.
    if indices[0] != 0:
        indices[0] = 0
    last_index = total - 1
    if indices[-1] != last_index:
        indices[-1] = last_index

    # De-duplicate while preserving order (in case rounding collapsed
    # adjacent indices) and re-sort.
    seen: set[int] = set()
    unique_indices: list[int] = []
    for idx in indices:
        if idx not in seen:
            seen.add(idx)
            unique_indices.append(idx)
    unique_indices.sort()

    sampled = [frame_paths[i] for i in unique_indices]

    logger.info(
        "Sampled %d frames from %d total (target=%d).",
        len(sampled),
        total,
        target_count,
    )
    return sampled
