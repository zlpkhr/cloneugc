const previewDefault = {
  en: "Hello, how are you?",
  ru: "Привет, как дела?",
};

const previewAudioButton = document.getElementById("preview-audio");
const creatorId = previewAudioButton.dataset.creatorId;
const language = previewAudioButton.dataset.language;

previewAudioButton.addEventListener("click", () => {
  window.prompt("Preview voice with following:", previewDefault[language]);
});
