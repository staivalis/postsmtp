from dataclasses import dataclass

from postsmtp.exceptions import ConfigurationError


@dataclass(frozen=True)
class SmtpConfig:
    smtp_server: str
    sender_email: str
    password: str
    smtp_port: int = 587
    username: str | None = None
    use_starttls: bool = True
    use_ssl: bool = False
    timeout_seconds: float = 30.0

    def __post_init__(self) -> None:
        smtp_server = self.smtp_server.strip() if isinstance(self.smtp_server, str) else ""
        sender_email = self.sender_email.strip() if isinstance(self.sender_email, str) else ""
        password = self.password.strip() if isinstance(self.password, str) else ""

        if not smtp_server:
            raise ConfigurationError("smtp_server is required")
        if not sender_email:
            raise ConfigurationError("sender_email is required")
        if not password:
            raise ConfigurationError("password is required")

        if not isinstance(self.smtp_port, int) or self.smtp_port <= 0:
            raise ConfigurationError("smtp_port must be a positive integer")
        if self.use_ssl and self.use_starttls:
            raise ConfigurationError("use_ssl and use_starttls cannot both be true")
        if self.timeout_seconds <= 0:
            raise ConfigurationError("timeout_seconds must be greater than zero")

        object.__setattr__(self, "smtp_server", smtp_server)
        object.__setattr__(self, "sender_email", sender_email)
        object.__setattr__(self, "password", password)
        if self.username is None:
            object.__setattr__(self, "username", sender_email)
