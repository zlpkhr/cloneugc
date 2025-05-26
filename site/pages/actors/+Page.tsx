import "media-chrome";
import {
  MediaControlBar,
  MediaController,
  MediaPlayButton
} from "media-chrome/react";

export default function ActorsPage() {
  const actors: { id: number; name: string; video: { url: string } }[] = [];

  return (
    <div className="flex">
      <aside className="sticky top-0 hidden h-screen bg-stone-100 p-7 sm:block">
        <nav className="flex flex-col gap-y-4">
          <a
            data-active="true"
            href="#"
            className="group flex w-full flex-col items-center justify-center gap-y-1"
          >
            <span className="material-symbols-rounded rounded-full px-3 py-1 group-hover:bg-stone-200 group-data-[active=true]:bg-pink-200 group-data-[active=true]:text-pink-800">
              comedy_mask
            </span>
            <span className="text-xl font-semibold group-data-[active=true]:text-pink-800">
              Actors
            </span>
          </a>
          <a
            data-active="false"
            href="#"
            className="group flex w-full flex-col items-center justify-center gap-y-1"
          >
            <span className="material-symbols-rounded rounded-full px-3 py-1 group-hover:bg-stone-200 group-data-[active=true]:bg-pink-200 group-data-[active=true]:text-pink-800">
              movie
            </span>
            <span className="text-xl font-semibold group-data-[active=true]:text-pink-800">
              Videos
            </span>
          </a>
        </nav>
      </aside>
      <div className="flex-1">
        <header className="sticky top-0 z-30 flex h-16 items-center justify-between bg-white px-4 shadow-sm sm:hidden">
          <button
            id="nav-trigger"
            className="material-symbols-rounded flex size-10 items-center justify-center rounded-full active:bg-stone-100"
          >
            menu
          </button>
        </header>
        <dialog
          id="nav"
          className="h-full max-h-full w-full max-w-xs bg-white backdrop:bg-black/30"
        >
          <header className="flex h-16 items-center justify-between px-4">
            <button
              id="close"
              className="material-symbols-rounded flex size-10 items-center justify-center rounded-full active:bg-stone-100"
            >
              menu_open
            </button>
          </header>
          <nav className="flex flex-col gap-y-4 px-4">
            <a
              data-active="true"
              href="#"
              className="group flex w-full items-center gap-x-2.5 rounded-full px-3 py-2 data-[active=false]:hover:bg-stone-200 data-[active=true]:bg-pink-200 data-[active=true]:text-pink-800"
            >
              <span className="material-symbols-rounded">comedy_mask</span>
              <span className="text-xl font-semibold">Actors</span>
            </a>
            <a
              data-active="false"
              href="#"
              className="group flex w-full items-center gap-x-2.5 rounded-full px-3 py-2 data-[active=false]:hover:bg-stone-200 data-[active=true]:bg-pink-200 data-[active=true]:text-pink-800"
            >
              <span className="material-symbols-rounded">movie</span>
              <span className="text-xl font-semibold">Videos</span>
            </a>
          </nav>
        </dialog>
        <header className="flex items-center justify-between px-7 pt-7">
          <hgroup>
            <h1 className="text-3xl font-bold">Available Actors</h1>
            <p className="text-lg font-medium text-stone-500">
              Click on actor to continue
            </p>
          </hgroup>
          <button
            id="create-actor-trigger"
            className="btn fixed right-5 bottom-7 z-20 shrink-0 shadow-lg sm:static sm:shadow-none"
          >
            Create Actor
          </button>
        </header>
        <dialog
          id="create-actor"
          className="mx-auto mt-auto w-full max-w-md rounded-t-xl rounded-l-xl rounded-r-xl rounded-b-none bg-white p-5 backdrop:bg-black/30 min-[28rem]:mb-auto min-[28rem]:rounded-b-xl"
        >
          <header>
            <hgroup className="flex items-center justify-between gap-x-2">
              <h4 className="text-2xl font-bold">Create Actor</h4>
              <button
                id="close"
                type="button"
                className="material-symbols-rounded flex size-10 items-center justify-center rounded-full active:bg-stone-100"
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
                      href={`#?actor_id=${actor.id}`}
                      className="text-xl font-semibold text-white text-shadow-xs hover:underline"
                    >
                      {actor.name}
                    </a>
                  </figcaption>
                  <MediaController className="aspect-[9/16] size-full rounded-xl">
                    <video
                      slot="media"
                      className="size-full rounded-xl object-cover"
                      src={actor.video.url}
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
              ))
            ) : (
              <p className="text-xl font-bold">No actors found.</p>
            )}
          </section>
        </main>
      </div>
    </div>
  );
}
