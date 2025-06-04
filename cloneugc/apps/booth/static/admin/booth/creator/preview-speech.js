import { previewSpeech } from "studio/preview-speech";

const previewDefault = {
  en: "Hello, how are you?",
  ru: "Привет, как дела?",
};

const previewSpeechBtn = document.querySelector("button#preview-speech");

const creatorId = previewSpeechBtn.dataset.creatorId;
const language = previewSpeechBtn.dataset.language;

previewSpeechBtn.addEventListener("click", async () => {
  const text = window.prompt(
    "Preview speech with following:",
    previewDefault[language],
  );

  if (!text) return;

  previewSpeechBtn.disabled = true;

  try {
    const blob = await previewSpeech(creatorId, text);

    const url = URL.createObjectURL(blob);
    const audio = new Audio(url);

    audio.play();

    audio.addEventListener("ended", () => {
      URL.revokeObjectURL(url);
    });
  } catch (error) {
    console.error("Failed to preview speech:", error);
    alert("Failed to preview the speech. See details in the console.");
  } finally {
    previewSpeechBtn.disabled = false;
  }
});
