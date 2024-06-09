import streamlit as st
import tempfile
import os
from text_to_speech import save as tts_save
from deep_translator import GoogleTranslator
from PyPDF2 import PdfReader

# Function to translate text using GoogleTranslator
def Gtranslator(text, target_lang):
    translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
    return translated

# Function to translate text from a PDF file using GoogleTranslator
def translate_file(file, target_lang):
    translated = GoogleTranslator(source='auto', target=target_lang).translate_file(file)
    return translated

# Function to convert text to speech and save it as an MP3 file
def text_to_speech(text, lang='en'):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmpfile:
        tts_save(text=text, lang=lang, slow=False, file=tmpfile.name, lang_check=False)
        return tmpfile.name

# Function to extract text from a PDF file
def extract_text_from_pdf(file):
    text = ""
    reader = PdfReader(file)
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text += page.extract_text()
    return text

# Main function to run the Streamlit app
def main():
    st.title("Translator & Narrator")

    # Languages supported by text-to-speech
    languages_tts_supported = {
        'Afrikaans': 'af',
        'Arabic': 'ar',
        'Bulgarian': 'bg',
        'Bengali': 'bn',
        'Bosnian': 'bs',
        'Catalan': 'ca',
        'Czech': 'cs',
        'Danish': 'da',
        'German': 'de',
        'Greek': 'el',
        'English': 'en',
        'Spanish': 'es',
        'Estonian': 'et',
        'Finnish': 'fi',
        'French': 'fr',
        'Gujarati': 'gu',
        'Hindi': 'hi',
        'Croatian': 'hr',
        'Hungarian': 'hu',
        'Indonesian': 'id',
        'Icelandic': 'is',
        'Italian': 'it',
        'Hebrew': 'iw',
        'Japanese': 'ja',
        'Javanese': 'jw',
        'Khmer': 'km',
        'Kannada': 'kn',
        'Korean': 'ko',
        'Latin': 'la',
        'Latvian': 'lv',
        'Malayalam': 'ml',
        'Marathi': 'mr',
        'Malay': 'ms',
        'Myanmar (Burmese)': 'my',
        'Nepali': 'ne',
        'Dutch': 'nl',
        'Norwegian': 'no',
        'Polish': 'pl',
        'Portuguese': 'pt',
        'Romanian': 'ro',
        'Russian': 'ru',
        'Sinhala': 'si',
        'Slovak': 'sk',
        'Albanian': 'sq',
        'Serbian': 'sr',
        'Sundanese': 'su',
        'Swedish': 'sv',
        'Swahili': 'sw',
        'Tamil': 'ta',
        'Telugu': 'te',
        'Thai': 'th',
        'Filipino': 'tl',
        'Turkish': 'tr',
        'Ukrainian': 'uk',
        'Urdu': 'ur',
        'Vietnamese': 'vi',
        'Chinese (Simplified)': 'zh-CN',
        'Chinese (Mandarin/Taiwan)': 'zh-TW',
        'Chinese (Mandarin)': 'zh'
    }


    # All languages supported by GoogleTranslator
    languages_translate_supported = {
        'Afrikaans': 'af', 
        'Albanian': 'sq', 
        'Amharic': 'am', 
        'Arabic': 'ar', 
        'Armenian': 'hy', 
        'Assamese': 'as', 
        'Aymara': 'ay', 
        'Azerbaijani': 'az', 
        'Bambara': 'bm', 
        'Basque': 'eu', 
        'Belarusian': 'be', 
        'Bengali': 'bn', 
        'Bhojpuri': 'bho', 
        'Bosnian': 'bs', 
        'Bulgarian': 'bg', 
        'Catalan': 'ca', 
        'Cebuano': 'ceb', 
        'Chichewa': 'ny', 
        'Chinese (simplified)': 'zh-CN', 
        'Chinese (traditional)': 'zh-TW', 
        'Corsican': 'co', 
        'Croatian': 'hr', 
        'Czech': 'cs', 
        'Danish': 'da', 
        'Dhivehi': 'dv', 
        'Dogri': 'doi', 
        'Dutch': 'nl', 
        'English': 'en', 
        'Esperanto': 'eo', 
        'Estonian': 'et',
        'Ewe': 'ee', 
        'Filipino': 'tl', 
        'Finnish': 'fi', 
        'French': 'fr', 
        'Frisian': 'fy', 
        'Galician': 'gl', 
        'Georgian': 'ka', 
        'German': 'de', 
        'Greek': 'el', 
        'Guarani': 'gn', 
        'Gujarati': 'gu', 
        'Haitian Creole': 'ht', 
        'Hausa': 'ha', 
        'Hawaiian': 'haw', 
        'Hebrew': 'iw', 
        'Hindi': 'hi', 
        'Hmong': 'hmn', 
        'Hungarian': 'hu', 
        'Icelandic': 'is', 
        'Igbo': 'ig', 
        'Ilocano': 'ilo', 
        'Indonesian': 'id', 
        'Irish': 'ga', 
        'Italian': 'it', 
        'Japanese': 'ja', 
        'Javanese': 'jw', 
        'Kannada': 'kn', 
        'Kazakh': 'kk', 
        'Khmer': 'km', 
        'Kinyarwanda': 'rw', 
        'Konkani': 'gom', 
        'Korean': 'ko', 
        'Krio': 'kri', 
        'Kurdish (Kurmanji)': 'ku', 
        'Kurdish (Sorani)': 'ckb', 
        'Kyrgyz': 'ky', 
        'Lao': 'lo', 
        'Latin': 'la', 
        'Latvian': 'lv', 
        'Lingala': 'ln', 
        'Lithuanian': 'lt', 
        'Luganda': 'lg', 
        'Luxembourgish': 'lb', 
        'Macedonian': 'mk', 
        'Maithili': 'mai', 
        'Malagasy': 'mg', 
        'Malay': 'ms', 
        'Malayalam': 'ml', 
        'Maltese': 'mt', 
        'Maori': 'mi', 
        'Marathi': 'mr', 
        'Meiteilon (Manipuri)': 'mni-Mtei', 
        'Mizo': 'lus', 
        'Mongolian': 'mn', 
        'Myanmar': 'my', 
        'Nepali': 'ne', 
        'Norwegian': 'no', 
        'Odia (Oriya)': 'or', 
        'Oromo': 'om', 
        'Pashto': 'ps', 
        'Persian': 'fa', 
        'Polish': 'pl', 
        'Portuguese': 'pt', 
        'Punjabi': 'pa', 
        'Quechua': 'qu', 
        'Romanian': 'ro', 
        'Russian': 'ru', 
        'Samoan': 'sm', 
        'Sanskrit': 'sa', 
        'Scots Gaelic': 'gd', 
        'Sepedi': 'nso', 
        'Serbian': 'sr', 
        'Sesotho': 'st', 
        'Shona': 'sn', 
        'Sindhi': 'sd', 
        'Sinhala': 'si', 
        'Slovak': 'sk', 
        'Slovenian': 'sl', 
        'Somali': 'so', 
        'Spanish': 'es',
        'Sundanese': 'su', 
        'Swahili': 'sw', 
        'Swedish': 'sv', 
        'Tajik': 'tg', 
        'Tamil': 'ta', 
        'Tatar': 'tt', 
        'Telugu': 'te', 
        'Thai': 'th', 
        'Tigrinya': 'ti', 
        'Tsonga': 'ts', 
        'Turkish': 'tr', 
        'Turkmen': 'tk', 
        'Twi': 'ak', 
        'Ukrainian': 'uk', 
        'Urdu': 'ur', 
        'Uyghur': 'ug', 
        'Uzbek': 'uz', 
        'Vietnamese': 'vi', 
        'Welsh': 'cy', 
        'Xhosa': 'xh', 
        'Yiddish': 'yi', 
        'Yoruba': 'yo', 
        'Zulu': 'zu'
        
        }

    selected_language = st.selectbox("Select language", options=list(languages_translate_supported.keys()))
    lang_code = languages_translate_supported[selected_language]

    tts_supported = lang_code in languages_tts_supported.values()

    option = st.radio("Select input method", ("Upload PDF", "Enter Text"))

    if option == "Upload PDF":
        uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
        if uploaded_file is not None:
            text = extract_text_from_pdf(uploaded_file)

            if st.button("Translate"):
                translated_text = translate_file(uploaded_file, lang_code)
                st.text_area("Translated Text", translated_text, height=200)

            if tts_supported:
                if st.button("Narrate"):
                    st.header("Original PDF Content Narration")
                    audio_file = text_to_speech(text, lang_code)
                    audio_data = open(audio_file, "rb").read()
                    st.audio(audio_data, format='audio/mp3')
                    st.download_button(label="Download Audio", data=audio_data, file_name="result.mp3", mime="audio/mp3")
                    os.remove(audio_file)

                if st.button("Translate & Narrate"):
                    st.header("Translated PDF Content Narration")
                    translated_text = translate_file(uploaded_file, lang_code)
                    audio_file = text_to_speech(translated_text, lang_code)
                    audio_data = open(audio_file, "rb").read()
                    st.audio(audio_data, format='audio/mp3')
                    st.download_button(label="Download Audio", data=audio_data, file_name="translated_result.mp3", mime="audio/mp3")
                    os.remove(audio_file)

    elif option == "Enter Text":
        text_input = st.text_area("Enter text here")
        
        if st.button("Translate"):
            if text_input:
                translated_text = Gtranslator(text_input, lang_code)
                st.text_area("Translated Text", translated_text, height=200)
            else:
                st.warning("Please enter some text before submitting.")
        
        if tts_supported:
            if st.button("Narrate"):
                if text_input:
                    audio_file = text_to_speech(text_input, lang_code)
                    audio_data = open(audio_file, "rb").read()
                    st.audio(audio_data, format='audio/mp3')
                    st.download_button(label="Download Audio", data=audio_data, file_name="result.mp3", mime="audio/mp3")
                    os.remove(audio_file)
                else:
                    st.warning("Please enter some text before submitting.")

            if st.button("Translate & Narrate"):
                if text_input:
                    translated_text = Gtranslator(text_input, lang_code)
                    st.text_area("Translated Text", translated_text, height=200)
                    audio_file = text_to_speech(translated_text, lang_code)
                    audio_data = open(audio_file, "rb").read()
                    st.audio(audio_data, format='audio/mp3')
                    st.download_button(label="Download Audio", data=audio_data, file_name="translated_result.mp3", mime="audio/mp3")
                    os.remove(audio_file)
                else:
                    st.warning("Please enter some text before submitting.")

if __name__ == "__main__":
    main()
