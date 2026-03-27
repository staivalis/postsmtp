import pytest

from postsmtp import ConfigurationError, SmtpConfig


def test_config_requires_fields() -> None:
    with pytest.raises(ConfigurationError):
        SmtpConfig(
            smtp_server="",
            sender_email="sender@example.com",
            password="x",
        )


def test_config_defaults_username_to_sender() -> None:
    config = SmtpConfig(
        smtp_server="smtp.example.com",
        sender_email="sender@example.com",
        password="x",
    )
    assert config.username == "sender@example.com"
