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
    "#prepare-script-trigger"
  );
  const scriptEl = document.querySelector("#script");

  prepareScriptTrigger.addEventListener("click", async () => {
    scriptEl.disabled = true;
    prepareScriptTrigger.disabled = true;

    try {
      if (scriptEl.value.length === 0) {
        alert("Enter a script first.");
        return;
      }

      const res = await fetch("/studio/prepare-script/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ script: scriptEl.value }),
      });

      const data = await res.json();
      scriptEl.value = data.preparedScript;
    } catch (error) {
      console.error("Failed to prepare script:", error);
      alert("Failed to prepare the script. Try again or contact support.");
    } finally {
      scriptEl.disabled = false;
      prepareScriptTrigger.disabled = false;
    }
  });
}
