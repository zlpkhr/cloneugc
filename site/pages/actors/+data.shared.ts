export async function data() {
  const response = await fetch(`${import.meta.env.VITE_APP_URL}/graphql/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json"
    },
    body: JSON.stringify({
      query: /* GraphQL */ `
        {
          actors {
            id
            name
            videoUrl
          }
        }
      `
    })
  });

  const { data } = await response.json();

  return {
    actors: data.actors as { id: number; name: string; videoUrl: string }[]
  };
}

export type ActorsData = Awaited<ReturnType<typeof data>>;
