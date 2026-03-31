"""Chunked translation using Google Translate (deep_translator)."""

from __future__ import annotations

import time

from deep_translator import GoogleTranslator
from deep_translator.exceptions import BaseError, RequestError

from translate_narrate.chunking import split_into_chunks
from translate_narrate.config import MAX_TRANSLATE_CHUNK_CHARS


def translate_text(text: str, target_lang: str, *, delay_seconds: float = 0.12) -> str:
    """
    Translate `text` into `target_lang` (Google language code), splitting into
    chunks so long documents stay within API limits.
    """
    chunks = split_into_chunks(text, MAX_TRANSLATE_CHUNK_CHARS)
    if not chunks:
        return ""
    translator = GoogleTranslator(source="auto", target=target_lang)
    out: list[str] = []
    for i, chunk in enumerate(chunks):
        if i > 0 and delay_seconds > 0:
            time.sleep(delay_seconds)
        try:
            out.append(translator.translate(chunk))
        except (BaseError, RequestError) as e:
            raise RuntimeError(f"Translation failed: {e}") from e
    return "\n\n".join(out)
