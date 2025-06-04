export async function previewSpeech(creatorId, text) {
  const res = await fetch("/studio/preview-speech/", {
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
        "Preview speech request has failed.",
      );
    }

    throw new Error("Preview speech request has failed.");
  }

  return res.blob();
}
