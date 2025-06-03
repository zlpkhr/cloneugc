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

  const reqUrl = new URL("/booth/preview-audio", window.location.origin);

  reqUrl.searchParams.set("creator_id", creatorId);
  reqUrl.searchParams.set("text", text);

  const res = await fetch(reqUrl);

  if (!res.ok) {
    previewAudioBtn.disabled = false;

    alert("Request failed. See details in the console.");

    const data = await res.json();

    console.error({ response: res, data });

    return;
  }

  const blob = await res.blob();

  const url = URL.createObjectURL(blob);
  const audio = new Audio(url);

  audio.play();

  audio.addEventListener("ended", () => {
    URL.revokeObjectURL(url);
  });

  previewAudioBtn.disabled = false;
});
