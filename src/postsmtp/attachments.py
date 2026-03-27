from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO
import mimetypes

from postsmtp.exceptions import ValidationError


@dataclass(frozen=True)
class Attachment:
    filename: str
    content_bytes: bytes
    content_type: str = "application/octet-stream"

    def __post_init__(self) -> None:
        filename = self.filename.strip() if isinstance(self.filename, str) else ""
        if not filename:
            raise ValidationError("attachment filename is required")
        if not isinstance(self.content_bytes, (bytes, bytearray)):
            raise ValidationError("attachment content_bytes must be bytes")
        if len(self.content_bytes) == 0:
            raise ValidationError("attachment content_bytes cannot be empty")
        if not isinstance(self.content_type, str) or "/" not in self.content_type:
            raise ValidationError("attachment content_type must be a valid MIME type")

        object.__setattr__(self, "filename", filename)
        object.__setattr__(self, "content_bytes", bytes(self.content_bytes))


def attachment_from_bytes(
    filename: str,
    data: bytes,
    content_type: str | None = None,
) -> Attachment:
    resolved_content_type = content_type or _guess_content_type(filename)
    return Attachment(
        filename=filename,
        content_bytes=data,
        content_type=resolved_content_type,
    )


def attachment_from_file(
    path: str | Path,
    filename: str | None = None,
    content_type: str | None = None,
) -> Attachment:
    file_path = Path(path)
    if not file_path.exists() or not file_path.is_file():
        raise ValidationError(f"attachment path not found: {file_path}")

    data = file_path.read_bytes()
    resolved_filename = filename or file_path.name
    resolved_content_type = content_type or _guess_content_type(resolved_filename)

    return Attachment(
        filename=resolved_filename,
        content_bytes=data,
        content_type=resolved_content_type,
    )


def attachment_from_stream(
    filename: str,
    stream: BinaryIO,
    content_type: str | None = None,
) -> Attachment:
    data = stream.read()
    if not isinstance(data, (bytes, bytearray)):
        raise ValidationError("stream must return bytes")
    resolved_content_type = content_type or _guess_content_type(filename)

    return Attachment(
        filename=filename,
        content_bytes=bytes(data),
        content_type=resolved_content_type,
    )


def _guess_content_type(filename: str) -> str:
    guessed, _ = mimetypes.guess_type(filename)
    return guessed or "application/octet-stream"
