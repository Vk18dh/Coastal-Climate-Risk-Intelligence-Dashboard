"""
Standardized exceptions for the provider layer.
"""

class ProviderError(Exception):
    """Base exception for all provider-related errors."""
    pass


class ProviderConnectionError(ProviderError):
    """Raised when the provider API cannot be reached or times out."""
    pass


class ProviderValidationError(ProviderError):
    """Raised when the provider returns an unexpected response structure."""
    pass


class ProviderAuthenticationError(ProviderError):
    """Raised when API keys are invalid or missing."""
    pass
