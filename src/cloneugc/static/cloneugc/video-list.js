let initBodyOverflow;
let initHtmlOverflow;

const navTrigger = document.querySelector("button#nav-trigger");
const nav = document.querySelector("dialog#nav");

navTrigger.addEventListener("click", () => {
  initBodyOverflow = document.body.style.overflow;
  initHtmlOverflow = document.documentElement.style.overflow;

  document.body.style.overflow = "hidden";
  document.documentElement.style.overflow = "hidden";

  nav.showModal();
});

nav.addEventListener("click", (event) => {
  const rect = nav.getBoundingClientRect();

  const outside =
    event.clientX < rect.left ||
    event.clientX > rect.right ||
    event.clientY < rect.top ||
    event.clientY > rect.bottom;

  if (outside) {
    nav.close();
  }
});

nav.addEventListener("close", () => {
  document.body.style.overflow = initBodyOverflow;
  document.documentElement.style.overflow = initHtmlOverflow;
});

const closeBtn = document.querySelector("dialog#nav button#close");

closeBtn.addEventListener("click", () => {
  nav.close();
});
