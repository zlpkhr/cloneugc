const previewDefault = {
  en: "Hello, how are you?",
  ru: "Привет, как дела?",
};

const previewAudioButton = document.getElementById("preview-audio");
const creatorId = previewAudioButton.dataset.creatorId;
const language = previewAudioButton.dataset.language;

previewAudioButton.addEventListener("click", async () => {
  const text = window.prompt(
    "Preview voice with following:",
    previewDefault[language]
  );
  if (!text) return;

  previewAudioButton.disabled = true;
  try {
    const params = new URLSearchParams({
      creator_id: creatorId,
      text: text,
    });
    const response = await fetch(`/booth/preview-audio?${params.toString()}`);
    const contentType = response.headers.get("content-type");
    if (!response.ok) {
      let errorMsg = "Unknown error";
      if (contentType && contentType.includes("application/json")) {
        const data = await response.json();
        if (data.errors) {
          errorMsg = Object.values(data.errors).flat().join("\n");
        } else if (data.error) {
          errorMsg = data.error;
        }
      } else {
        errorMsg = await response.text();
      }
      alert(errorMsg);
      return;
    }
    if (contentType && contentType.startsWith("audio/")) {
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      const audio = new Audio(url);
      audio.play();
      audio.onended = () => {
        URL.revokeObjectURL(url);
      };
    } else {
      alert("Unexpected response from server.");
    }
  } catch (err) {
    alert("Network error: " + err);
  } finally {
    previewAudioButton.disabled = false;
  }
});
