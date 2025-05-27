export async function data() {
  const response = await fetch("http://localhost:8000/graphql/", {
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
