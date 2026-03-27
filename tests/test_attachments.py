from pathlib import Path

from postsmtp import attachment_from_bytes, attachment_from_file


def test_attachment_from_bytes() -> None:
    attachment = attachment_from_bytes("notes.txt", b"hello")
    assert attachment.filename == "notes.txt"
    assert attachment.content_bytes == b"hello"


def test_attachment_from_file(tmp_path: Path) -> None:
    file_path = tmp_path / "a.txt"
    file_path.write_text("abc", encoding="utf-8")

    attachment = attachment_from_file(file_path)
    assert attachment.filename == "a.txt"
    assert attachment.content_bytes == b"abc"
