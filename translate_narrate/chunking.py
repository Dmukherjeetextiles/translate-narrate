"""Split long text into chunks that stay under provider limits."""

from __future__ import annotations

from translate_narrate.config import MAX_INPUT_CHARS


def split_into_chunks(text: str, max_chars: int) -> list[str]:
    """
    Split `text` into segments of at most `max_chars`, preferring paragraph
    and sentence boundaries when possible.
    """
    if max_chars < 1:
        raise ValueError("max_chars must be positive")
    text = text.strip()
    if not text:
        return []
    if len(text) > MAX_INPUT_CHARS:
        raise ValueError(f"Input exceeds maximum length ({MAX_INPUT_CHARS:,} characters).")

    if len(text) <= max_chars:
        return [text]

    chunks: list[str] = []
    remaining = text

    while remaining:
        if len(remaining) <= max_chars:
            chunks.append(remaining.strip())
            break

        segment = remaining[:max_chars]
        cut = _best_break_index(segment)
        piece = remaining[:cut].strip()
        if not piece:
            piece = remaining[:max_chars].strip()
            cut = max_chars
        chunks.append(piece)
        remaining = remaining[cut:].lstrip()

    return [c for c in chunks if c]


def _best_break_index(segment: str) -> int:
    """Largest index in `segment` to split on, favoring natural boundaries."""
    max_len = len(segment)
    for sep in ("\n\n", "\n", ". ", "! ", "? ", "; ", ", ", " "):
        idx = segment.rfind(sep, 0, max_len)
        if idx > max_len // 4:
            return idx + len(sep)
    return max_len
