const micButton = document.getElementById("micButton");
const status = document.getElementById("status");
const userMessage = document.getElementById("userMessage");
const aiMessage = document.getElementById("aiMessage");

let mediaRecorder;
let audioChunks = [];
let isRecording = false;

micButton.addEventListener("click", async () => {

    if (!isRecording) {

        try {

            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

            mediaRecorder = new MediaRecorder(stream);

            audioChunks = [];

            mediaRecorder.start();

            isRecording = true;

            micButton.innerHTML = "⏹ Stop Recording";
            status.innerHTML = "🎤 Listening...";

            mediaRecorder.ondataavailable = (event) => {
                audioChunks.push(event.data);
            };

            mediaRecorder.onstop = async () => {

                status.innerHTML = "🤖 Thinking...";

                const audioBlob = new Blob(audioChunks, { type: "audio/wav" });

                const formData = new FormData();
                formData.append("audio", audioBlob, "input.wav");

                try {

                    const response = await fetch("/chat", {
                        method: "POST",
                        body: formData
                    });

                    const data = await response.json();

                    userMessage.style.display = "block";
                    aiMessage.style.display = "block";

                    userMessage.innerHTML = "👤 <b>You:</b><br>" + data.text;
                    aiMessage.innerHTML = "🤖 <b>AI Voice Assistant :</b><br>" + data.reply;

                    status.innerHTML = "🔊 Speaking...";

                    const audio = new Audio(data.audio + "?t=" + new Date().getTime());

                    audio.play();

                    audio.onended = () => {
                        status.innerHTML = "✅ Ready for another question.";
                    };

                }

                catch (err) {

                    console.error(err);
                    status.innerHTML = "❌ Error communicating with server.";

                }

            };

        }

        catch (err) {

            alert("Please allow microphone access.");

        }

    }

    else {

        mediaRecorder.stop();

        isRecording = false;

        micButton.innerHTML = "🎤 Start Conversation";

    }

});