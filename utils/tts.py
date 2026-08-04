import os
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

load_dotenv()

speech_key = os.getenv("AZURE_SPEECH_KEY")
service_region = os.getenv("AZURE_SPEECH_REGION")

import tempfile

OUTPUT_FILE = os.path.join(
    tempfile.gettempdir(),
    "output.mp3"
)


def speak(text):
    try:
        # Make sure the audio folder exists
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

        speech_config = speechsdk.SpeechConfig(
            subscription=speech_key,
            region=service_region
        )

        # Voice
        speech_config.speech_synthesis_voice_name = "en-US-AriaNeural"

        audio_config = speechsdk.audio.AudioOutputConfig(
            filename=OUTPUT_FILE
        )

        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config,
            audio_config=audio_config
        )

        result = synthesizer.speak_text_async(text).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("Speech generated successfully!")
            return OUTPUT_FILE

        else:
            print("Azure Speech Error:", result.reason)
            return None

    except Exception as e:
        print("Azure TTS Error:", e)
        return None