import streamlit as st

from utils.recorder import record_audio
from utils.speech import speech_to_text
from utils.llm import ask_llm
from utils.tts import speak

st.set_page_config(
    page_title="AI Voice Assistant",
    page_icon="🎤",
    layout="centered"
)

st.title("🎤 AI Voice Assistant")
st.write("Click the button below and ask your question.")

if st.button("🎙 Start Recording"):

    # Record
    with st.spinner("Recording..."):
        audio_path = record_audio()

    # Speech-to-Text
    with st.spinner("Converting Speech to Text..."):
        text = speech_to_text(audio_path)

    st.subheader("🗣 You Said")
    st.write(text)

    # AI Response
    reply = ask_llm(text)

    st.subheader("🤖 Assistant")
    st.write(reply)

    # Generate Voice
    audio_file = speak(reply)

    # Play Audio
    if audio_file:
        with open(audio_file, "rb") as audio:
            st.audio(audio.read(), format="audio/mp3", autoplay=True)
    else:
        st.error("Voice generation failed.")