import { previewSpeech } from "studio/preview-speech";
import { prepareScript } from "studio/prepare-script";
import { createScriptEditor } from "studio/script-editor";

const scriptEl = document.querySelector("[name=script]");
const scriptEditorEl = document.querySelector("#script-editor");

const editor = createScriptEditor(scriptEditorEl);

editor.on("update", ({ editor }) => {
  scriptEl.value = editor.getText();
});

const creatorInput = document.querySelector("#creator-input");
const creatorVideos = document.querySelectorAll("#creator-video");

const firstVideo = creatorVideos.item(0);

creatorInput.value = firstVideo.dataset.creatorId;
firstVideo.dataset.selected = "true";

for (const video of creatorVideos) {
  video.addEventListener("click", () => {
    for (const video of creatorVideos) {
      video.dataset.selected = "false";
    }

    creatorInput.value = video.dataset.creatorId;
    video.dataset.selected = "true";
  });
}

{
  const prepareScriptTrigger = document.querySelector(
    "#prepare-script-trigger",
  );

  prepareScriptTrigger.addEventListener("click", async () => {
    scriptEl.disabled = true;
    prepareScriptTrigger.disabled = true;

    if (scriptEl.value.length === 0) {
      alert("Enter a script first.");
      return;
    }

    try {
      const preparedScript = await prepareScript(scriptEl.value);

      scriptEl.value = preparedScript;
    } catch (error) {
      console.error("Failed to prepare script:", error);
      alert("Failed to prepare the script. Try again or contact support.");
    } finally {
      scriptEl.disabled = false;
      prepareScriptTrigger.disabled = false;
    }
  });
}

const previewSpeechTrigger = document.querySelector("#preview-speech-trigger");

previewSpeechTrigger.addEventListener("click", async () => {
  previewSpeechTrigger.disabled = true;

  try {
    const blob = await previewSpeech(creatorInput.value, editor.getText());
    const url = URL.createObjectURL(blob);
    const audio = new Audio(url);

    audio.addEventListener("ended", () => {
      URL.revokeObjectURL(url);
    });

    audio.play();
  } catch (error) {
    console.error("Failed to preview speech:", error);
    alert("Failed to preview the speech. Try again or contact support.");
  } finally {
    previewSpeechTrigger.disabled = false;
  }
});
