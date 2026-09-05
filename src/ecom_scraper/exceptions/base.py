"""Exception hierarchy for the crawler engine."""


class EcomScraperError(Exception):
    """Base class for all ecom-scraper errors."""


class ConfigurationError(EcomScraperError):
    """Raised when runtime configuration is missing or invalid."""


class RequestError(EcomScraperError):
    """Raised when a request is malformed or cannot be built."""


class FetchError(EcomScraperError):
    """Raised when a request cannot be fetched."""


class ParseError(EcomScraperError):
    """Raised when a response cannot be parsed."""


class ValidationError(EcomScraperError):
    """Raised when parsed data fails validation."""


class PersistenceError(EcomScraperError):
    """Raised when data cannot be persisted."""


class TaskError(EcomScraperError):
    """Raised when a crawl task fails."""


class PlatformError(EcomScraperError):
    """Raised for platform-specific failures."""
