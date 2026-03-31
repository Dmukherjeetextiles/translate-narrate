"""Translator & Narrator — translate and read aloud PDF or pasted text."""

from translate_narrate.narration import synthesize_mp3
from translate_narrate.pdf import extract_text_from_pdf
from translate_narrate.translation import translate_text

__all__ = ["extract_text_from_pdf", "translate_text", "synthesize_mp3"]
