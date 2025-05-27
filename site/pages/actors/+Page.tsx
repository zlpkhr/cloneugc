import { useEffect, useRef, useState } from "react";
import { useData } from "vike-react/useData";
import type { ActorsData } from "./+data";
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

export default function ActorsPage() {
  const { actors } = useData<ActorsData>();

  // Dialog state
  const [isCreateActorOpen, setCreateActorOpen] = useState(false);
  const createActorDialogRef = useRef<HTMLDialogElement>(null);
  const createActorTriggerRef = useRef<HTMLButtonElement>(null);

  // Overflow lock helpers (only for create actor dialog)
  useEffect(() => {
    if (isCreateActorOpen) {
      const prevBody = document.body.style.overflow;
      const prevHtml = document.documentElement.style.overflow;
      document.body.style.overflow = "hidden";
      document.documentElement.style.overflow = "hidden";
      return () => {
        document.body.style.overflow = prevBody;
        document.documentElement.style.overflow = prevHtml;
      };
    }
  }, [isCreateActorOpen]);

  // Show/hide create actor dialog
  useEffect(() => {
    const dialog = createActorDialogRef.current;
    if (!dialog) return;
    if (isCreateActorOpen) {
      if (!dialog.open) dialog.showModal();
      // Hide trigger on mobile
      if (
        window.matchMedia("(max-width: 640px)").matches &&
        createActorTriggerRef.current
      ) {
        createActorTriggerRef.current.style.visibility = "hidden";
      }
    } else {
      if (dialog.open) dialog.close();
      if (createActorTriggerRef.current) {
        createActorTriggerRef.current.style.visibility = "";
      }
    }
  }, [isCreateActorOpen]);

  // Click outside to close for create actor dialog
  useEffect(() => {
    const abortController = new AbortController();
    if (isCreateActorOpen) {
      window.addEventListener(
        "mousedown",
        (event) => {
          if (isCreateActorOpen && createActorDialogRef.current) {
            const rect = createActorDialogRef.current.getBoundingClientRect();
            if (
              event.target instanceof Node &&
              createActorDialogRef.current.open &&
              (event.clientX < rect.left ||
                event.clientX > rect.right ||
                event.clientY < rect.top ||
                event.clientY > rect.bottom)
            ) {
              setCreateActorOpen(false);
            }
          }
        },
        { signal: abortController.signal }
      );
    }
    return () => {
      abortController.abort();
    };
  }, [isCreateActorOpen]);

  // Dialog close event (esc, etc)
  useEffect(() => {
    const createDialog = createActorDialogRef.current;
    const abortController = new AbortController();
    if (createDialog) {
      createDialog.addEventListener("close", () => setCreateActorOpen(false), {
        signal: abortController.signal
      });
    }
    return () => {
      abortController.abort();
    };
  }, []);

  return (
    <>
      <header className="flex items-center justify-between px-7 pt-7">
        <hgroup>
          <h1 className="text-3xl font-bold">Available Actors</h1>
          <p className="text-lg font-medium text-stone-500">
            Click on actor to continue
          </p>
        </hgroup>
        <button
          ref={createActorTriggerRef}
          className="btn fixed right-5 bottom-7 z-20 shrink-0 shadow-lg sm:static sm:shadow-none"
          onClick={() => setCreateActorOpen(true)}
        >
          Create Actor
        </button>
      </header>
      <dialog
        ref={createActorDialogRef}
        className="mx-auto mt-auto w-full max-w-md rounded-t-xl rounded-l-xl rounded-r-xl rounded-b-none bg-white p-5 backdrop:bg-black/30 min-[28rem]:mb-auto min-[28rem]:rounded-b-xl"
      >
        <header>
          <hgroup className="flex items-center justify-between gap-x-2">
            <h4 className="text-2xl font-bold">Create Actor</h4>
            <button
              type="button"
              className="material-symbols-rounded flex size-10 items-center justify-center rounded-full active:bg-stone-100"
              onClick={() => setCreateActorOpen(false)}
            >
              close
            </button>
          </hgroup>
          <p className="mt-2 text-lg font-medium text-stone-500">
            For best results, center the face and ensure that the torso is
            visible.
          </p>
        </header>
        <form
          className="mt-6"
          method="post"
          action="#"
          encType="multipart/form-data"
        >
          {/* CSRF token not needed in React; handle in logic if needed */}
          <input
            type="text"
            name="name"
            placeholder="Name"
            required
            className="h-11 w-full rounded-lg bg-stone-100 px-2.5 text-xl font-semibold focus:outline-3 focus:outline-pink-800"
          />
          <input
            type="file"
            name="video"
            accept="video/*"
            required
            className="mt-5 w-full file:mr-4 file:h-11 file:rounded-full file:border file:border-stone-200 file:bg-white file:px-3.5 file:text-lg file:font-semibold active:file:bg-stone-100"
            capture="user"
          />
          <div className="mt-8 sm:flex sm:items-center sm:justify-end">
            <button type="submit" className="btn w-full sm:w-auto">
              Create
            </button>
          </div>
        </form>
      </dialog>
      <main className="mt-7 px-7 pb-10 sm:mt-10">
        <section className="grid grid-cols-[repeat(auto-fit,minmax(--spacing(60),1fr))] gap-5">
          {actors.length > 0 ? (
            actors.map((actor) => (
              <figure className="relative" key={actor.id}>
                <figcaption className="absolute inset-x-0 top-0 z-10 rounded-t-xl bg-linear-to-b from-black/20 to-black/0 p-4">
                  <a
                    href={`/create-video?actor_id=${actor.id}`}
                    className="text-xl font-semibold text-white text-shadow-xs hover:underline"
                  >
                    {actor.name}
                  </a>
                </figcaption>
                <MediaController className="aspect-[9/16] size-full rounded-xl">
                  <video
                    slot="media"
                    className="size-full rounded-xl object-cover"
                    src={actor.videoUrl}
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
              </figure>
            ))
          ) : (
            <p className="text-xl font-bold">No actors found.</p>
          )}
        </section>
      </main>
    </>
  );
}
