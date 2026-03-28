# translate-narrate
This is a pdf or text narrater with translation features.

https://translator-narrator.streamlit.app/

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

For Streamlit Community Cloud, set the main file to `app.py`. Long inputs are split automatically (translation and narration use chunked requests). **ffmpeg** is required when narration spans multiple chunks (installed via `packages.txt` on Cloud, or install locally and ensure it is on `PATH`).
