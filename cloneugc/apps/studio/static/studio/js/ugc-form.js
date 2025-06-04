import { previewAudio } from "studio/preview-audio";
import { prepareScript } from "studio/prepare-script";

{
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
}

{
  const prepareScriptTrigger = document.querySelector(
    "#prepare-script-trigger",
  );
  const scriptEl = document.querySelector("#script");

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

{
  const previewAudioTrigger = document.querySelector("#preview-audio-trigger");
  const scriptEl = document.querySelector("#script");
  const creatorInput = document.querySelector("#creator-input");

  previewAudioTrigger.addEventListener("click", async () => {
    previewAudioTrigger.disabled = true;

    try {
      const blob = await previewAudio(creatorInput.value, scriptEl.value);

      const url = URL.createObjectURL(blob);
      const audio = new Audio(url);

      audio.play();

      audio.addEventListener("ended", () => {
        URL.revokeObjectURL(url);
      });
    } catch (error) {
      console.error("Failed to preview audio:", error);
      alert("Failed to preview the audio. Try again or contact support.");
    } finally {
      previewAudioTrigger.disabled = false;
    }
  });
}
