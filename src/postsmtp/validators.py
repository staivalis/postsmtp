import re
from collections.abc import Sequence

from postsmtp.exceptions import ValidationError

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def normalize_emails(value: str | Sequence[str], field_name: str) -> list[str]:
    if isinstance(value, str):
        values = [value]
    elif isinstance(value, Sequence):
        values = list(value)
    else:
        raise ValidationError(f"{field_name} must be a string or list of strings")

    normalized: list[str] = []
    for raw in values:
        if not isinstance(raw, str):
            raise ValidationError(f"{field_name} must contain only strings")

        candidate = raw.strip()
        if not candidate:
            raise ValidationError(f"{field_name} contains an empty value")
        if not EMAIL_REGEX.match(candidate):
            raise ValidationError(f"invalid email in {field_name}: {candidate}")

        normalized.append(candidate)

    if field_name == "to_emails" and not normalized:
        raise ValidationError("to_emails cannot be empty")

    return _dedupe(normalized)


def validate_subject(subject: str) -> str:
    if not isinstance(subject, str):
        raise ValidationError("subject must be a string")
    clean = subject.strip()
    if not clean:
        raise ValidationError("subject cannot be empty")
    if len(clean) > 255:
        raise ValidationError("subject too long (max 255)")
    return clean


def validate_body(body: str | None, html_body: str | None) -> tuple[str, str | None]:
    if body is not None and not isinstance(body, str):
        raise ValidationError("body must be a string")
    if html_body is not None and not isinstance(html_body, str):
        raise ValidationError("html_body must be a string")

    clean_body = body.strip() if isinstance(body, str) else ""
    clean_html = html_body.strip() if isinstance(html_body, str) else ""

    if not clean_body and not clean_html:
        raise ValidationError("at least one of body or html_body is required")

    if not clean_body:
        clean_body = "This email includes HTML content."

    return clean_body, (clean_html or None)


def dedupe_recipients(
    to_emails: list[str],
    cc_emails: list[str],
    bcc_emails: list[str],
) -> tuple[list[str], list[str], list[str]]:
    seen: set[str] = set()
    unique_to: list[str] = []
    unique_cc: list[str] = []
    unique_bcc: list[str] = []

    for email in to_emails:
        if email not in seen:
            seen.add(email)
            unique_to.append(email)

    for email in cc_emails:
        if email not in seen:
            seen.add(email)
            unique_cc.append(email)

    for email in bcc_emails:
        if email not in seen:
            seen.add(email)
            unique_bcc.append(email)

    return unique_to, unique_cc, unique_bcc


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result
