from unittest.mock import MagicMock, patch

from postsmtp import SmtpConfig, SmtpMailer


@patch("postsmtp.mailer.smtplib.SMTP")
def test_mailer_send_calls_smtp(mock_smtp: MagicMock) -> None:
    smtp_client = MagicMock()
    mock_smtp.return_value.__enter__.return_value = smtp_client

    config = SmtpConfig(
        smtp_server="smtp.example.com",
        smtp_port=587,
        sender_email="sender@example.com",
        password="app-password",
    )
    mailer = SmtpMailer(config)

    mailer.send(
        to_emails=["to@example.com"],
        subject="Test",
        body="Hello",
    )

    smtp_client.starttls.assert_called_once()
    smtp_client.login.assert_called_once_with("sender@example.com", "app-password")
    smtp_client.send_message.assert_called_once()
