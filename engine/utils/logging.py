"""
Reusable logging utilities for the DescribeX caption engine.

Provides a configured logger that should be used everywhere instead
of ``print()`` statements.  Uses only the Python standard library.

Usage:
    from engine.utils.logging import get_logger

    logger = get_logger(__name__)
    logger.info("Pipeline started.")
"""

import logging
import sys

# Flag to ensure we only attach the root handler once.
_configured: bool = False

# Default format aligned with the architecture doc's logging examples.
_LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def _configure_root_logger(level: str = "INFO") -> None:
    """Attach a console handler to the ``engine`` root logger.

    Called automatically the first time :func:`get_logger` is invoked.
    Subsequent calls are no-ops.
    """
    global _configured  # noqa: PLW0603
    if _configured:
        return

    root = logging.getLogger("engine")
    root.setLevel(level.upper())

    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(level.upper())
    handler.setFormatter(logging.Formatter(_LOG_FORMAT, datefmt=_DATE_FORMAT))

    root.addHandler(handler)
    _configured = True


def get_logger(name: str, level: str | None = None) -> logging.Logger:
    """Return a configured :class:`logging.Logger`.

    On first call the ``engine`` root logger is configured with a console
    handler.  The *level* defaults to the value of
    :pyattr:`EngineConfig.log_level` (loaded lazily to avoid circular
    imports).

    Args:
        name: Logger name — typically ``__name__`` of the calling module.
        level: Optional override for the log level.

    Returns:
        A ready-to-use :class:`logging.Logger` instance.
    """
    if not _configured:
        # Lazy import to avoid a circular dependency at module load time.
        from engine.utils.config import get_config

        effective_level = level or get_config().log_level
        _configure_root_logger(effective_level)

    return logging.getLogger(name)
