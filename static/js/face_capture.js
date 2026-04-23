
// Activation de la webcam

const video = document.querySelector("#video");

if (video) {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => video.srcObject = stream)
        .catch(err => console.error("Erreur webcam:", err));
}

// Capture pour l'inscription

const captureBtn = document.querySelector("#capture-face");

if (captureBtn) {
    captureBtn.onclick = () => {
        const canvas = document.createElement("canvas");
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;

        const ctx = canvas.getContext("2d");
        ctx.drawImage(video, 0, 0);

        const dataUrl = canvas.toDataURL("image/jpeg");

        // On met l'image base64 dans le champ caché
        document.querySelector("#face_image").value = dataUrl;

        alert("Visage capturé !");
    };
}


// Capture pour le LOGIN facial

async function captureAndLogin(email) {
    if (!video) {
        alert("Webcam non détectée");
        return;
    }

    // Capture image
    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext("2d").drawImage(video, 0, 0);

    const base64Image = canvas.toDataURL("image/jpeg");

    // Envoyer au backend
    const res = await fetch("/login/face", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image: base64Image, email })
    });

    const data = await res.json();

    alert(data.message);

    if (data.success) {
        window.location.href = "/";
    }
}
