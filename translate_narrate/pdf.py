"""Extract plain text from PDF uploads."""

from __future__ import annotations

from typing import BinaryIO

from PyPDF2 import PdfReader


def extract_text_from_pdf(file: BinaryIO) -> str:
    file.seek(0)
    reader = PdfReader(file)
    parts: list[str] = []
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            parts.append(extracted)
    return "\n\n".join(parts).strip()
