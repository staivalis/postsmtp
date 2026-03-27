from email.message import EmailMessage

from postsmtp.attachments import Attachment
from postsmtp.config import SmtpConfig


def build_message(
    config: SmtpConfig,
    to_emails: list[str],
    cc_emails: list[str],
    subject: str,
    body: str,
    html_body: str | None,
    attachments: list[Attachment],
    reply_to: str | None,
) -> EmailMessage:
    message = EmailMessage()
    message["From"] = config.sender_email
    message["To"] = ", ".join(to_emails)
    if cc_emails:
        message["Cc"] = ", ".join(cc_emails)
    if reply_to:
        message["Reply-To"] = reply_to
    message["Subject"] = subject

    if html_body:
        message.set_content(body)
        message.add_alternative(html_body, subtype="html")
    else:
        message.set_content(body)

    for attachment in attachments:
        maintype, subtype = attachment.content_type.split("/", 1)
        message.add_attachment(
            attachment.content_bytes,
            maintype=maintype,
            subtype=subtype,
            filename=attachment.filename,
        )

    return message
