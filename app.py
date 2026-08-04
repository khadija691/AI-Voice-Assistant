import tempfile

from flask import Flask, render_template, request, jsonify, send_file
import os

from utils.speech import speech_to_text
from utils.llm import ask_llm
from utils.tts import speak

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    import traceback

    try:
        print("STEP 1")

        audio = request.files["audio"]
        print("STEP 2")

        import tempfile

audio_path = os.path.join(tempfile.gettempdir(), "input.wav")
audio.save(audio_path)
print("STEP 3")

        text = speech_to_text(audio_path)
        print("Recognized:", text)
        print("STEP 4")

        reply = ask_llm(text)
        print("Reply:", reply)
        print("STEP 5")

        speak(reply)
        print("Speech finished")
        print("STEP 6")

        return jsonify({
            "text": text,
            "reply": reply,
            "audio": "/audio"
        })

    except Exception:
        print(traceback.format_exc())
        return jsonify({"error": traceback.format_exc()}), 500


@import tempfile

@app.route("/audio")
def audio():
    return send_file(
        os.path.join(tempfile.gettempdir(), "output.mp3"),
        mimetype="audio/mpeg"
    )

if __name__ == "__main__":
    app.run(debug=True)