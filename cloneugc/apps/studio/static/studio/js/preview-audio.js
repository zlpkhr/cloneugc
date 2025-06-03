export async function previewAudio(creatorId, text) {
  const reqUrl = new URL("/studio/preview-audio/", window.location.origin);

  reqUrl.searchParams.set("creator_id", creatorId);
  reqUrl.searchParams.set("text", text);

  const res = await fetch(reqUrl);

  if (!res.ok) {
    const data = await res.json();

    throw new AggregateError(data.errors, "Preview audio request has failed.");
  }

  return res.blob();
}
