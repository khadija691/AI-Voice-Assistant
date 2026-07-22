from faster_whisper import WhisperModel

# Load the model only once
model = WhisperModel("base", device="cpu", compute_type="int8")


def speech_to_text(audio_file):
    segments, _ = model.transcribe(audio_file)

    text = ""

    for segment in segments:
        text += segment.text + " "

    return text.strip()