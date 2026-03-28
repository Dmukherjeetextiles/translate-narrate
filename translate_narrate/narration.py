"""Text-to-speech with chunking and optional MP3 merging (pydub + ffmpeg)."""

from __future__ import annotations

import os
import tempfile
from io import BytesIO

from gtts import gTTS
from gtts.lang import tts_langs

from translate_narrate.chunking import split_into_chunks
from translate_narrate.config import MAX_TTS_CHUNK_CHARS


def _normalize_gtts_lang(lang_code: str) -> str:
    """Map translator codes to a gTTS-supported language key."""
    langs = tts_langs()
    if lang_code in langs:
        return lang_code
    lower = lang_code.lower()
    if lower in langs:
        return lower
    # e.g. zh-cn vs zh-CN — gTTS uses mixed case keys
    for key in langs:
        if key.lower() == lower:
            return key
    base = lang_code.split("-")[0]
    if base in langs:
        return base
    raise ValueError(f"Language {lang_code!r} is not supported for narration (gTTS).")


def synthesize_mp3(text: str, lang_code: str) -> bytes:
    """Return MP3 bytes for `text`, using chunked synthesis when needed."""
    g_lang = _normalize_gtts_lang(lang_code)
    chunks = split_into_chunks(text, MAX_TTS_CHUNK_CHARS)
    if not chunks:
        raise ValueError("No text to narrate.")

    if len(chunks) == 1:
        buf = BytesIO()
        gTTS(text=chunks[0], lang=g_lang).write_to_fp(buf)
        return buf.getvalue()

    # pydub (and ffmpeg) only needed when merging multiple MP3 segments.
    from pydub import AudioSegment

    tmp_paths: list[str] = []
    try:
        for chunk in chunks:
            fd, path = tempfile.mkstemp(suffix=".mp3")
            os.close(fd)
            tmp_paths.append(path)
            gTTS(text=chunk, lang=g_lang).save(path)

        combined = AudioSegment.from_mp3(tmp_paths[0])
        for path in tmp_paths[1:]:
            combined += AudioSegment.from_mp3(path)

        out = BytesIO()
        combined.export(out, format="mp3")
        return out.getvalue()
    finally:
        for path in tmp_paths:
            try:
                os.unlink(path)
            except OSError:
                pass
