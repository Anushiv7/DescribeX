"""
Custom exception hierarchy for the DescribeX caption engine.

All engine-specific exceptions inherit from :class:`DescribeXError`
so callers can catch a single base class when desired.

These are placeholders — implementations in later phases will raise
them with meaningful messages and context.
"""


class DescribeXError(Exception):
    """Base exception for all DescribeX engine errors."""


class ConfigurationError(DescribeXError):
    """Raised when engine configuration is invalid or missing."""


class ValidationError(DescribeXError):
    """Raised when input validation fails (e.g. unsupported video format)."""


class ProviderError(DescribeXError):
    """Raised when an AI provider request fails (timeout, auth, bad response)."""


class PreprocessingError(DescribeXError):
    """Raised when video preprocessing fails (extraction, sampling)."""


class FormattingError(DescribeXError):
    """Raised when caption formatting or parsing fails."""


class ExportError(DescribeXError):
    """Raised when caption export fails."""

