class MergeError(Exception):
    """Raised when an error occurs during PDF merging."""
    pass

class EmailError(Exception):
    """Raised when an error occurs during email sending."""
    pass

class ConfigurationError(Exception):
    """Raised when there is an issue with the configuration."""
    pass
