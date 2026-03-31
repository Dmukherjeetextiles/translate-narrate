"""Streamlit UI for Translator & Narrator."""

from __future__ import annotations

import streamlit as st

from translate_narrate.chunking import split_into_chunks
from translate_narrate.config import MAX_INPUT_CHARS, MAX_TRANSLATE_CHUNK_CHARS, MAX_TTS_CHUNK_CHARS
from translate_narrate.languages import (
    LANGUAGES_TRANSLATE_SUPPORTED,
    is_tts_available_for_translate_code,
)
from translate_narrate.narration import synthesize_mp3
from translate_narrate.pdf import extract_text_from_pdf
from translate_narrate.translation import translate_text


def _render_limits_note(text: str) -> None:
    text_len = len(text or "")
    if not text.strip():
        st.caption(f"Paste text or upload a PDF (up to **{MAX_INPUT_CHARS:,}** characters).")
        return
    if text_len > MAX_INPUT_CHARS:
        st.caption(
            f"Length: **{text_len:,}** — over limit (**{MAX_INPUT_CHARS:,}**). "
            "Trim the content before translating or narrating."
        )
        return
    tr = len(split_into_chunks(text, MAX_TRANSLATE_CHUNK_CHARS))
    tt = len(split_into_chunks(text, MAX_TTS_CHUNK_CHARS))
    st.caption(
        f"Length: **{text_len:,}** characters (max **{MAX_INPUT_CHARS:,}**). "
        f"API batches for this text — translate: **{tr}**, narration: **{tt}** "
        f"(≤{MAX_TRANSLATE_CHUNK_CHARS} / ≤{MAX_TTS_CHUNK_CHARS} chars per request)."
    )


def _audio_player(audio_bytes: bytes, download_name: str, *, widget_prefix: str) -> None:
    st.audio(audio_bytes, format="audio/mp3")
    st.download_button(
        "Download MP3",
        data=audio_bytes,
        file_name=download_name,
        mime="audio/mp3",
        key=f"{widget_prefix}_mp3_dl",
    )


def main() -> None:
    st.set_page_config(page_title="Translator & Narrator", layout="wide")
    st.title("Translator & Narrator")
    st.markdown("Translate PDF or pasted text and listen to narration in supported languages.")

    with st.sidebar:
        st.header("Language")
        selected = st.selectbox(
            "Target language",
            options=sorted(LANGUAGES_TRANSLATE_SUPPORTED.keys()),
            key="target_lang_name",
        )
        lang_code = LANGUAGES_TRANSLATE_SUPPORTED[selected]
        tts_ok = is_tts_available_for_translate_code(lang_code)
        if tts_ok:
            st.success("Narration available for this language.")
        else:
            st.info("Translation only — gTTS does not support narration for this language.")

    input_mode = st.radio("Input", ("Paste or type text", "Upload PDF"), horizontal=True)

    text_content = ""
    pdf_name = ""

    if input_mode == "Paste or type text":
        text_content = st.text_area(
            "Text",
            height=280,
            placeholder="Paste or type content to translate and/or narrate…",
            key="main_text",
        )
    else:
        uploaded = st.file_uploader("PDF file", type=["pdf"])
        if uploaded is not None:
            pdf_name = uploaded.name
            with st.spinner("Extracting text from PDF…"):
                try:
                    text_content = extract_text_from_pdf(uploaded)
                except Exception as e:
                    st.error(f"Could not read PDF: {e}")
                    text_content = ""
            if not text_content.strip():
                st.warning("No extractable text found (scanned PDFs need OCR elsewhere first).")

    text_len = len(text_content or "")
    _render_limits_note(text_content)

    col1, col2, col3 = st.columns(3)
    with col1:
        do_translate = st.button("Translate", type="primary", use_container_width=True)
    with col2:
        do_narrate = st.button(
            "Narrate (original)",
            use_container_width=True,
            disabled=not tts_ok or not text_content.strip(),
        )
    with col3:
        do_both = st.button(
            "Translate & narrate",
            use_container_width=True,
            disabled=not tts_ok or not text_content.strip(),
        )

    if not text_content.strip() and (do_translate or do_narrate or do_both):
        st.warning("Add text or upload a PDF with extractable text first.")
        return

    if text_len > MAX_INPUT_CHARS:
        st.error(f"Text is too long (>{MAX_INPUT_CHARS:,} characters). Trim the content and try again.")
        return

    if do_translate:
        with st.spinner("Translating…"):
            try:
                translated = translate_text(text_content, lang_code)
            except RuntimeError as e:
                st.error(str(e))
            else:
                st.subheader("Translation")
                st.text_area("Translated text", translated, height=320, key="out_translate")

    if do_narrate and tts_ok:
        with st.spinner("Generating audio…"):
            try:
                audio = synthesize_mp3(text_content, lang_code)
            except (ValueError, OSError) as e:
                st.error(f"Narration failed: {e}")
            else:
                st.subheader("Narration (original language)")
                name = "narration_original.mp3" if not pdf_name else f"narration_{pdf_name.rsplit('.', 1)[0]}.mp3"
                _audio_player(audio, name, widget_prefix="narrate_orig")

    if do_both and tts_ok:
        with st.spinner("Translating and generating audio…"):
            try:
                translated = translate_text(text_content, lang_code)
            except RuntimeError as e:
                st.error(str(e))
                return
            st.subheader("Translation")
            st.text_area("Translated text", translated, height=240, key="out_both_text")
            try:
                audio = synthesize_mp3(translated, lang_code)
            except (ValueError, OSError) as e:
                st.error(f"Narration failed: {e}")
                return
            st.subheader("Narration (translated)")
            name = "narration_translated.mp3"
            _audio_player(audio, name, widget_prefix="narrate_trans")


if __name__ == "__main__":
    main()
