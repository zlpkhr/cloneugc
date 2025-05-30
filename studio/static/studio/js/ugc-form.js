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
