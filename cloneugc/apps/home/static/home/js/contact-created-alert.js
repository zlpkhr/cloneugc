const params = new URLSearchParams(window.location.search);

if (params.get("contact_saved") === "True") {
  alert("Contact saved! We will reach out soon.");
} else if (params.get("contact_saved") === "False") {
  alert("Contact not saved. Please try again.");
}

window.history.replaceState(
  {},
  "",
  window.location.pathname + window.location.hash,
);
