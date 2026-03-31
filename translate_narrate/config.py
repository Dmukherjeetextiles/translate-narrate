"""Application limits and tunables."""

# Google Translate (via deep_translator) and gTTS stay under typical ~5k char limits per request.
MAX_TRANSLATE_CHUNK_CHARS = 4500
MAX_TTS_CHUNK_CHARS = 4500

# Soft guard for pasted text / extracted PDF size (characters).
MAX_INPUT_CHARS = 2_000_000
