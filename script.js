async function uploadImage() {
    const input = document.getElementById('imageInput');
    const result = document.getElementById('result');
    const preview = document.getElementById('preview');
    const loading = document.getElementById('loading');
    const imagePreviewContainer = document.getElementById('imagePreviewContainer');

    if (input.files.length === 0) {
        alert("Please select an image.");
        return;
    }

    const file = input.files[0];

    // Show image preview
    const reader = new FileReader();
    reader.onload = function(e) {
        preview.src = e.target.result;
        preview.style.display = "block";
        preview.style.transform = "scale(1.05)";
    };
    reader.readAsDataURL(file);

    // Show loading spinner
    loading.style.display = "inline-block";
    result.innerText = "";

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch("http://localhost:8000/predict", {
            method: "POST",
            body: formData
        });

        if (!response.ok) {
            throw new Error("Prediction failed.");
        }

        const data = await response.json();
        loading.style.display = "none";
        result.innerText = `Prediction: ${data.class} (${(data.confidence * 100).toFixed(2)}% confidence)`;
    } catch (error) {
        loading.style.display = "none";
        result.innerText = "Error: " + error.message;
        console.error(error);
    }
}
