const triggerBtn = document.querySelector("button#create-actor-trigger");
const dialog = document.querySelector("dialog#create-actor");
const closeBtn = document.querySelector("dialog#create-actor button#close");

let initBodyOverflow;
let initHtmlOverflow;

let initTriggerVisibility;

closeBtn.addEventListener("click", () => {
  dialog.close();
});

triggerBtn.addEventListener("click", () => {
  initBodyOverflow = document.body.style.overflow;
  initHtmlOverflow = document.documentElement.style.overflow;
  initTriggerVisibility = triggerBtn.style.visibility;

  document.body.style.overflow = "hidden";
  document.documentElement.style.overflow = "hidden";

  dialog.showModal();

  if (window.matchMedia("(max-width: 640px)").matches) {
    triggerBtn.style.visibility = "hidden";
  }
});

dialog.addEventListener("click", (event) => {
  const rect = dialog.getBoundingClientRect();

  const outside =
    event.clientX < rect.left ||
    event.clientX > rect.right ||
    event.clientY < rect.top ||
    event.clientY > rect.bottom;

  if (outside) {
    dialog.close();

    document.body.style.overflow = initBodyOverflow;
    document.documentElement.style.overflow = initHtmlOverflow;

    if (window.matchMedia("(max-width: 640px)").matches) {
      triggerBtn.style.visibility = initTriggerVisibility;
    }
  }
});
