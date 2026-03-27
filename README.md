# postsmtp

`postsmtp` is a lightweight synchronous SMTP email library for Python.

Security policy: see [SECURITY.md](SECURITY.md).

- Send plain text or HTML emails
- Optional CC/BCC/Reply-To
- Optional attachments from files, bytes, or streams
- STARTTLS by default, SSL mode optional

## Install

```bash
pip install postsmtp
```

## Quick Start

```python
from postsmtp import SmtpConfig, send_email

config = SmtpConfig(
    smtp_server="smtp.office365.com",
    smtp_port=587,
    sender_email="sender@example.com",
    password="your-app-password",
    use_starttls=True,
)

send_email(
    config=config,
    to_emails=["john@example.com"],
    subject="Hello",
    body="Email sent with postsmtp.",
)
```

## HTML Example

```python
from postsmtp import SmtpConfig, SmtpMailer

config = SmtpConfig(
    smtp_server="smtp.gmail.com",
    smtp_port=587,
    sender_email="sender@gmail.com",
    password="app-password",
    use_starttls=True,
)

mailer = SmtpMailer(config)
mailer.send(
    to_emails=["john@example.com"],
    subject="HTML Demo",
    body="Fallback plain text body.",
    html_body="<h2>Hello</h2><p>This is an HTML email.</p>",
)
```

## Two Attachments Example

```python
from postsmtp import (
    SmtpConfig,
    SmtpMailer,
    attachment_from_file,
)

config = SmtpConfig(
    smtp_server="smtp.office365.com",
    smtp_port=587,
    sender_email="sender@example.com",
    password="app-password",
    use_starttls=True,
)

attachment_1 = attachment_from_file("invoice_1001.pdf")
attachment_2 = attachment_from_file("invoice_1002.pdf")

mailer = SmtpMailer(config)
mailer.send(
    to_emails=["finance@example.com"],
    subject="Invoices",
    body="Attached are two invoices.",
    attachments=[attachment_1, attachment_2],
)
```

## API

### `SmtpConfig`

Required:

- `smtp_server`
- `sender_email`
- `password`

Optional:

- `smtp_port` (default: `587`)
- `username` (default: `sender_email`)
- `use_starttls` (default: `True`)
- `use_ssl` (default: `False`)
- `timeout_seconds` (default: `30.0`)

### `SmtpMailer.send(...)`

Required:

- `to_emails`
- `subject`
- `body` or `html_body`

Optional:

- `html_body`
- `cc_emails`
- `bcc_emails`
- `reply_to`
- `attachments`

### Attachment helpers

- `attachment_from_file(path, filename=None, content_type=None)`
- `attachment_from_bytes(filename, data, content_type=None)`
- `attachment_from_stream(filename, stream, content_type=None)`

## Exceptions

- `ConfigurationError`
- `ValidationError`
- `SmtpConnectionError`
- `AuthenticationError`
- `SendError`

All inherit from `PostSmtpError`.

## Development

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -e ".[dev]"
pytest
```

## License

MIT
