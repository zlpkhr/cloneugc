export async function previewAudio(creatorId, text) {
  const res = await fetch("/studio/preview-audio/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ creatorId, text }),
  });

  if (!res.ok) {
    if (res.status < 500) {
      const data = await res.json();

      throw new AggregateError(
        data.errors,
        "Preview audio request has failed.",
      );
    }

    throw new Error("Preview audio request has failed.");
  }

  return res.blob();
}
