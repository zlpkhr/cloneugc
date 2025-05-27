export async function data() {
  const response = await fetch("http://localhost:3000/graphql/", {
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
