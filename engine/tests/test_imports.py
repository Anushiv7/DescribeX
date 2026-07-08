"""
Smoke / import tests for Phase 1.

These verify that the engine package structure is correctly installed
and that the core classes can be imported and instantiated.
"""

import logging

# ------------------------------------------------------------------
# Import tests
# ------------------------------------------------------------------


def test_import_caption_engine() -> None:
    """CaptionEngine should be importable from engine.core."""
    from engine.core.caption_engine import CaptionEngine

    assert CaptionEngine is not None


def test_import_config() -> None:
    """EngineConfig and get_config should be importable from engine.utils."""
    from engine.utils.config import EngineConfig, get_config

    assert EngineConfig is not None
    assert callable(get_config)


def test_import_logger() -> None:
    """get_logger should be importable from engine.utils."""
    from engine.utils.logging import get_logger

    assert callable(get_logger)


def test_import_exceptions() -> None:
    """Custom exception classes should be importable from engine.utils."""
    from engine.utils.exceptions import (
        ConfigurationError,
        DescribeXError,
        ProviderError,
        ValidationError,
    )

    assert issubclass(ConfigurationError, DescribeXError)
    assert issubclass(ValidationError, DescribeXError)
    assert issubclass(ProviderError, DescribeXError)


def test_import_top_level_version() -> None:
    """engine.__version__ should be available."""
    from engine import __version__

    assert isinstance(__version__, str)
    assert __version__ == "0.1.0"


# ------------------------------------------------------------------
# Instantiation tests
# ------------------------------------------------------------------


def test_caption_engine_instantiates() -> None:
    """CaptionEngine should instantiate with default config."""
    from engine.core.caption_engine import CaptionEngine

    engine = CaptionEngine()
    assert engine is not None
    assert engine.config is not None


def test_get_logger_returns_logger() -> None:
    """get_logger should return a stdlib Logger instance."""
    from engine.utils.logging import get_logger

    logger = get_logger("test")
    assert isinstance(logger, logging.Logger)


def test_generate_captions_raises_not_implemented() -> None:
    """generate_captions should raise NotImplementedError in Phase 1."""
    import pytest

    from engine.core.caption_engine import CaptionEngine

    engine = CaptionEngine()
    with pytest.raises(NotImplementedError):
        engine.generate_captions("/fake/video.mp4")
