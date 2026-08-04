import os
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

load_dotenv()

speech_key = os.getenv("AZURE_SPEECH_KEY")
service_region = os.getenv("AZURE_SPEECH_REGION")


def speech_to_text(audio_file):

    speech_config = speechsdk.SpeechConfig(
        subscription=speech_key,
        region=service_region
    )

    audio_config = speechsdk.audio.AudioConfig(filename=audio_file)

    recognizer = speechsdk.SpeechRecognizer(
        speech_config=speech_config,
        audio_config=audio_config
    )

    result = recognizer.recognize_once()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text

    return ""