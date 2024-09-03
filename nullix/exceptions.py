# nullix/exceptions.py


class NullixError(Exception):
    """Base exception class for Nullix project."""


class DistroNotSupportedError(NullixError):
    """Raised when the detected distribution is not supported."""


class PackageInstallationError(NullixError):
    """Raised when package installation fails."""


class PackageUpdateError(NullixError):
    """Raised when package update fails."""


class ConfigurationError(NullixError):
    """Raised when there's an error in the configuration."""
