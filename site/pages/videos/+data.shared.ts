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
          generations {
            id
            videoUrl
            status
            createdAt
          }
        }
      `
    })
  });

  const { data } = (await response.json()) as {
    data: {
      generations: {
        id: number;
        videoUrl: string;
        status: string;
        createdAt: string;
      }[];
    };
  };

  return {
    generations: data.generations.map((gen) => ({
      ...gen,
      createdAt: new Date(gen.createdAt)
    }))
  };
}

export type VideosData = Awaited<ReturnType<typeof data>>;
