import os
import streamlit as st
from streamlit_mic_recorder import mic_recorder

from utils.speech import speech_to_text
from utils.llm import ask_llm
from utils.tts import speak

st.set_page_config(
    page_title="AI Voice Assistant",
    page_icon="🎤",
    layout="centered"
)

st.title("🎤 AI Voice Assistant")
st.write("Click below and ask your question.")

audio = mic_recorder(
    start_prompt="🎙 Start Recording",
    stop_prompt="⏹ Stop Recording",
    key="mic"
)

if audio:

    os.makedirs("audio", exist_ok=True)

    audio_path = "audio/input.wav"

    with open(audio_path, "wb") as f:
        f.write(audio["bytes"])

    with st.spinner("Listening..."):
        text = speech_to_text(audio_path)

    st.subheader("🗣 You Said")
    st.write(text)

    with st.spinner("Thinking..."):
        reply = ask_llm(text)

    st.subheader("🤖 Assistant")
    st.write(reply)

    with st.spinner("Generating Voice..."):
        audio_file = speak(reply)

    if audio_file:
        st.audio(audio_file, format="audio/mp3", autoplay=True)
    else:
        st.error("Voice generation failed.")