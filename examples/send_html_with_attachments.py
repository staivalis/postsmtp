from postsmtp import SmtpConfig, SmtpMailer, attachment_from_file

config = SmtpConfig(
    smtp_server="smtp.office365.com",
    smtp_port=587,
    sender_email="sender@example.com",
    password="app-password",
    use_starttls=True,
)

mailer = SmtpMailer(config)
mailer.send(
    to_emails=["recipient@example.com"],
    subject="HTML with two attachments",
    body="Fallback plain text content.",
    html_body="<h3>Hello</h3><p>See attached files.</p>",
    attachments=[
        attachment_from_file("invoice_1001.pdf"),
        attachment_from_file("invoice_1002.pdf"),
    ],
)
