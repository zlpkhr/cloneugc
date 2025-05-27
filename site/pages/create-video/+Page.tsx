import { useData } from "vike-react/useData";
import type { CreateVideoData } from "./+data.client";
import { clientOnly } from "vike-react/clientOnly";
import type { FormEventHandler } from "react";
import { navigate } from "vike/client/router";

const MediaControlBar = clientOnly(() =>
  import("media-chrome/react").then((m) => m.MediaControlBar)
);
const MediaController = clientOnly(() =>
  import("media-chrome/react").then((m) => m.MediaController)
);
const MediaPlayButton = clientOnly(() =>
  import("media-chrome/react").then((m) => m.MediaPlayButton)
);

async function createGeneration(input: { actorId: string; script: string }) {
  const response = await fetch("/graphql/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json"
    },
    body: JSON.stringify({
      query: /* GraphQL */ `
        mutation CreateGeneration($input: GenerationInput!) {
          createGeneration(input: $input) {
            id
          }
        }
      `,
      variables: {
        input
      }
    })
  });

  const { data } = (await response.json()) as {
    data: {
      createGeneration: {
        id: string;
      };
    };
  };

  return data.createGeneration.id;
}
export default function CreateVideoPage() {
  const data = useData<CreateVideoData>();

  if (!data) {
    return <div>Actor not found</div>;
  }

  const handleSubmit: FormEventHandler<HTMLFormElement> = async (e) => {
    e.preventDefault();

    const formData = new FormData(e.currentTarget);
    const script = formData.get("script");

    if (!script) {
      throw new Error("Script is required");
    }

    await createGeneration({
      actorId: data.actor.id,
      script: script.toString()
    });

    navigate("/videos");
  };

  return (
    <div className="flex h-screen">
      <aside className="relative contents">
        <a
          href="/actors"
          className="bg-media-control hover:bg-media-control-hover absolute top-4 left-4 z-10 flex size-11 items-center justify-center rounded-full"
        >
          <span className="material-symbols-rounded text-media-text">
            arrow_back
          </span>
        </a>
        <MediaController className="aspect-square size-full flex-1">
          <video
            slot="media"
            className="size-full object-contain"
            src={data.actor.videoUrl}
          />
          <MediaControlBar className="p-4">
            <MediaPlayButton className="rounded-full p-2.5">
              <span slot="play" className="material-symbols-rounded">
                play_arrow
              </span>
              <span slot="pause" className="material-symbols-rounded">
                pause
              </span>
            </MediaPlayButton>
          </MediaControlBar>
        </MediaController>
      </aside>
      <main className="w-lg bg-white p-7">
        <hgroup>
          <h2 className="text-2xl font-bold">{data.actor.name}</h2>
          <p className="text-lg font-medium text-stone-500">
            Created {data.actor.createdAt}
          </p>
        </hgroup>
        <form onSubmit={handleSubmit} method="post" className="mt-6">
          <textarea
            name="script"
            id="script"
            className="w-full rounded-lg bg-stone-100 p-4 text-xl font-semibold focus:outline-3 focus:outline-pink-800"
            placeholder="Enter your script here..."
            rows={8}
            required
          />
          <div className="mt-8 flex justify-end">
            <button
              type="submit"
              className="h-11 rounded-full bg-pink-800 px-3.5 text-lg font-semibold text-white"
            >
              Create Video
            </button>
          </div>
        </form>
      </main>
    </div>
  );
}
