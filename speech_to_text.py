import whisper
import streamlit as st

@st.cache_resource 
def load_whisper():
    return whisper.load_model("base")

model = load_whisper()

def transcript(audio_path, txt_path):
    results = model.transcribe(audio_path)
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(results["text"])
    f.close()
