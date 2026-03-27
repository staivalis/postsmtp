from postsmtp import SmtpConfig, send_email

config = SmtpConfig(
    smtp_server="smtp.office365.com",
    smtp_port=587,
    sender_email="sender@example.com",
    password="app-password",
    use_starttls=True,
)

send_email(
    config=config,
    to_emails=["recipient@example.com"],
    subject="Plain text test",
    body="Hello from postsmtp.",
)
