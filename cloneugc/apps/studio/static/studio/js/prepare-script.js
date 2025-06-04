export async function prepareScript(script) {
  const res = await fetch("/studio/prepare-script/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ script }),
  });

  if (!res.ok) {
    throw new Error("Prepare script request failed.");
  }

  const data = await res.json();

  return data.preparedScript;
}
