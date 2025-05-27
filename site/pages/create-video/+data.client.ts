import type { PageContext } from "vike/types";

export async function data(pageContext: PageContext) {
  const actorId = pageContext.urlParsed.search["actor_id"];

  const response = await fetch("/graphql/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json"
    },
    body: JSON.stringify({
      query: /* GraphQL */ `
        query GetActor($id: String!) {
          actor(id: $id) {
            id
            name
            videoUrl
            createdAt
          }
        }
      `,
      variables: {
        id: actorId
      }
    })
  });

  const { data } = (await response.json()) as {
    data: {
      actor: {
        id: string;
        name: string;
        videoUrl: string;
        createdAt: string;
      };
    };
  };

  return {
    actor: {
      ...data.actor,
      createdAt: new Date(data.actor.createdAt).toLocaleDateString("en-US", {
        month: "long",
        day: "numeric",
        year: "numeric"
      })
    }
  };
}

export type CreateVideoData = Awaited<ReturnType<typeof data> | undefined>;
