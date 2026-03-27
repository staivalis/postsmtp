class PostSmtpError(Exception):
    """Base exception for all postsmtp errors."""


class ConfigurationError(PostSmtpError):
    """Raised for invalid SMTP configuration."""


class ValidationError(PostSmtpError):
    """Raised when email input validation fails."""


class SmtpConnectionError(PostSmtpError):
    """Raised when SMTP connection cannot be established."""


class AuthenticationError(PostSmtpError):
    """Raised when SMTP authentication fails."""


class SendError(PostSmtpError):
    """Raised when sending fails after connection/authentication."""
