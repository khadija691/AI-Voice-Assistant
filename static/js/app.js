const micButton = document.getElementById("micButton");

let recorder;
let chunks = [];
let recording = false;

micButton.onclick = async () => {

    if (!recording) {

        const stream = await navigator.mediaDevices.getUserMedia({
            audio: true
        });

        recorder = new MediaRecorder(stream);

        chunks = [];

        recorder.ondataavailable = e => {
            chunks.push(e.data);
        };

        recorder.onstop = async () => {

            const blob = new Blob(chunks, {
                type: "audio/wav"
            });

            const form = new FormData();

            form.append("audio", blob, "input.wav");

            micButton.innerHTML = "🤖 Thinking...";

            const response = await fetch("/chat", {
                method: "POST",
                body: form
            });

            const data = await response.json();

            document.getElementById("userText").innerHTML = data.text;

            document.getElementById("botText").innerHTML = data.reply;

            new Audio("/audio?" + Date.now()).play();

            micButton.innerHTML = "🎤 Start Conversation";
        };

        recorder.start();

        recording = true;

        micButton.innerHTML = "🔴 Stop Recording";

    } else {

        recording = false;

        recorder.stop();

    }

};