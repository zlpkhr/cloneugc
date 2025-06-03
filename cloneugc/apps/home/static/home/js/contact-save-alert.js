const params = new URLSearchParams(window.location.search);

if (params.get("contact_saved") === "true") {
  alert("Contact saved! We will reach out soon.");
}

window.history.replaceState(
  {},
  "",
  window.location.pathname + window.location.hash
);
