import smtplib
import socket
from collections.abc import Sequence

from postsmtp.attachments import Attachment
from postsmtp.config import SmtpConfig
from postsmtp.exceptions import (
    AuthenticationError,
    SendError,
    SmtpConnectionError,
    ValidationError,
)
from postsmtp.message import build_message
from postsmtp.validators import (
    dedupe_recipients,
    normalize_emails,
    validate_body,
    validate_subject,
)


class SmtpMailer:
    def __init__(self, config: SmtpConfig) -> None:
        self.config = config

    def send(
        self,
        to_emails: str | Sequence[str],
        subject: str,
        body: str | None = None,
        *,
        html_body: str | None = None,
        cc_emails: str | Sequence[str] | None = None,
        bcc_emails: str | Sequence[str] | None = None,
        attachments: Sequence[Attachment] | None = None,
        reply_to: str | None = None,
    ) -> None:
        to_list = normalize_emails(to_emails, "to_emails")
        cc_list = normalize_emails(cc_emails or [], "cc_emails")
        bcc_list = normalize_emails(bcc_emails or [], "bcc_emails")
        to_list, cc_list, bcc_list = dedupe_recipients(to_list, cc_list, bcc_list)

        clean_subject = validate_subject(subject)
        clean_body, clean_html_body = validate_body(body, html_body)
        clean_attachments = self._validate_attachments(attachments)
        clean_reply_to = self._validate_reply_to(reply_to)

        message = build_message(
            config=self.config,
            to_emails=to_list,
            cc_emails=cc_list,
            subject=clean_subject,
            body=clean_body,
            html_body=clean_html_body,
            attachments=clean_attachments,
            reply_to=clean_reply_to,
        )

        all_recipients = to_list + cc_list + bcc_list
        self._send_message(message, all_recipients)

    def _send_message(self, message, recipients: list[str]) -> None:
        smtp_cls = smtplib.SMTP_SSL if self.config.use_ssl else smtplib.SMTP

        try:
            with smtp_cls(
                self.config.smtp_server,
                self.config.smtp_port,
                timeout=self.config.timeout_seconds,
            ) as client:
                if self.config.use_starttls and not self.config.use_ssl:
                    client.ehlo()
                    client.starttls()
                    client.ehlo()

                client.login(self.config.username, self.config.password)
                client.send_message(
                    message,
                    from_addr=self.config.sender_email,
                    to_addrs=recipients,
                )
        except smtplib.SMTPAuthenticationError as error:
            raise AuthenticationError("SMTP authentication failed") from error
        except (socket.timeout, OSError, smtplib.SMTPConnectError) as error:
            raise SmtpConnectionError("Failed to connect to SMTP server") from error
        except smtplib.SMTPException as error:
            raise SendError(f"SMTP send failed: {error}") from error

    @staticmethod
    def _validate_attachments(
        attachments: Sequence[Attachment] | None,
    ) -> list[Attachment]:
        if attachments is None:
            return []
        result: list[Attachment] = []
        for item in attachments:
            if not isinstance(item, Attachment):
                raise ValidationError("attachments must contain Attachment objects")
            result.append(item)
        return result

    @staticmethod
    def _validate_reply_to(reply_to: str | None) -> str | None:
        if reply_to is None:
            return None
        if not isinstance(reply_to, str) or not reply_to.strip():
            raise ValidationError("reply_to must be a non-empty string")
        return reply_to.strip()


def send_email(
    config: SmtpConfig,
    to_emails: str | Sequence[str],
    subject: str,
    body: str | None = None,
    *,
    html_body: str | None = None,
    cc_emails: str | Sequence[str] | None = None,
    bcc_emails: str | Sequence[str] | None = None,
    attachments: Sequence[Attachment] | None = None,
    reply_to: str | None = None,
) -> None:
    SmtpMailer(config).send(
        to_emails=to_emails,
        subject=subject,
        body=body,
        html_body=html_body,
        cc_emails=cc_emails,
        bcc_emails=bcc_emails,
        attachments=attachments,
        reply_to=reply_to,
    )
