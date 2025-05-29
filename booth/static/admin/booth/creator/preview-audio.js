const previewDefault = {
  en: "Hello, how are you?",
  ru: "Привет, как дела?",
};

const previewAudioButton = document.getElementById("preview-audio");

const creatorId = previewAudioButton.dataset.creatorId;
const language = previewAudioButton.dataset.language;

if (!creatorId || !language) {
  previewAudioButton.disabled = true;
  throw new Error("Missing creatorId or language in data attributes.");
}

previewAudioButton.addEventListener("click", async () => {
  const text = window.prompt(
    "Preview voice with following:",
    previewDefault[language]
  );
  if (!text) return;

  previewAudioButton.disabled = true;
  try {
    const response = await fetch(
      `/booth/preview-audio?creator_id=${creatorId}&text=${text}`
    );

    if (!response.ok) {
      let errorMsg = "Unknown error";
      const data = await response.json();
      if (data.errors) {
        errorMsg = Object.values(data.errors).flat().join("\n");
      } else if (data.error) {
        errorMsg = data.error;
      }

      alert(errorMsg);
      return;
    }

    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    const audio = new Audio(url);
    audio.play();
    audio.onended = () => {
      URL.revokeObjectURL(url);
    };
  } catch (err) {
    alert("Network error: " + err);
  } finally {
    previewAudioButton.disabled = false;
  }
});
