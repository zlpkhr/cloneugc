import { previewAudio } from "studio/preview-audio";

const previewDefault = {
  en: "Hello, how are you?",
  ru: "Привет, как дела?",
};

const previewAudioBtn = document.querySelector("button#preview-audio");

const creatorId = previewAudioBtn.dataset.creatorId;
const language = previewAudioBtn.dataset.language;

previewAudioBtn.addEventListener("click", async () => {
  const text = window.prompt(
    "Preview voice with following:",
    previewDefault[language],
  );

  if (!text) return;

  previewAudioBtn.disabled = true;

  try {
    const blob = await previewAudio(creatorId, text);

    const url = URL.createObjectURL(blob);
    const audio = new Audio(url);

    audio.play();

    audio.addEventListener("ended", () => {
      URL.revokeObjectURL(url);
    });
  } catch (error) {
    console.error("Failed to preview audio:", error);
    alert("Request failed. See details in the console.");
  } finally {
    previewAudioBtn.disabled = false;
  }
});
