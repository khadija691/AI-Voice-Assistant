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

    audio = request.files["audio"]

    os.makedirs("audio", exist_ok=True)

    audio_path = "audio/input.wav"

    audio.save(audio_path)

    text = speech_to_text(audio_path)

    reply = ask_llm(text)

    audio_file = speak(reply)

    return jsonify({
        "text": text,
        "reply": reply,
        "audio": "/audio"
    })


@app.route("/audio")
def audio():
    return send_file("audio/output.mp3", mimetype="audio/mpeg")


if __name__ == "__main__":
    app.run(debug=True)