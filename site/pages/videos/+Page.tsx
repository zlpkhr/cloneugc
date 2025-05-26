import { clientOnly } from "vike-react/clientOnly";

const MediaControlBar = clientOnly(() =>
  import("media-chrome/react").then((m) => m.MediaControlBar)
);
const MediaController = clientOnly(() =>
  import("media-chrome/react").then((m) => m.MediaController)
);
const MediaPlayButton = clientOnly(() =>
  import("media-chrome/react").then((m) => m.MediaPlayButton)
);

export default function VideosPage() {
  const generations = [] as {
    id: string;
    video: {
      url: string;
    };
    created_at: string;
    status: string;
  }[];

  return (
    <div className="flex-1">
      <hgroup className="px-7 pt-7">
        <h1 className="text-3xl font-bold">Your Videos</h1>
        <p className="text-lg font-medium text-stone-500">
          Generated videos will appear here
        </p>
      </hgroup>
      <main className="mt-7 px-7 pb-10 sm:mt-10">
        <section className="grid grid-cols-[repeat(auto-fit,minmax(--spacing(60),1fr))] gap-5">
          {generations.map((gen) =>
            gen.video ? (
              <figure className="relative">
                <figcaption className="absolute inset-x-0 top-0 z-10 rounded-t-xl bg-linear-to-b from-black/20 to-black/0 p-4 text-xl font-semibold text-white text-shadow-xs">
                  {gen.created_at}
                </figcaption>
                <a
                  href={gen.video.url}
                  className="bg-media-control hover:bg-media-control-hover absolute right-4 bottom-4 z-10 flex size-11 items-center justify-center rounded-full"
                >
                  <span className="material-symbols-rounded text-media-text">
                    download
                  </span>
                </a>
                <MediaController className="aspect-[9/16] size-full rounded-xl">
                  <video
                    slot="media"
                    className="size-full rounded-xl object-cover"
                    src={gen.video.url}
                  ></video>
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
              </figure>
            ) : (
              <div className="flex aspect-[9/16] items-center justify-center rounded-xl border-2 border-dashed border-stone-200 bg-stone-100 p-4">
                <span className="text-center text-xl font-semibold text-stone-500">
                  {gen.status}
                </span>
              </div>
            )
          )}
        </section>
      </main>
    </div>
  );
}
