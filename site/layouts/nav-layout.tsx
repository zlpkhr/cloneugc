import type { ReactNode } from "react";
import { useEffect, useRef, useState } from "react";
import { usePageContext } from "vike-react/usePageContext";

type NavLayoutProps = {
  children: ReactNode;
};

export function NavLayout(props: NavLayoutProps) {
  const pageContext = usePageContext();
  // Dialog state for navigation
  const [isNavOpen, setNavOpen] = useState(false);
  const navDialogRef = useRef<HTMLDialogElement>(null);

  // Overflow lock helpers for nav
  useEffect(() => {
    if (isNavOpen) {
      const prevBody = document.body.style.overflow;
      const prevHtml = document.documentElement.style.overflow;
      document.body.style.overflow = "hidden";
      document.documentElement.style.overflow = "hidden";
      return () => {
        document.body.style.overflow = prevBody;
        document.documentElement.style.overflow = prevHtml;
      };
    }
  }, [isNavOpen]);

  // Show/hide nav dialog
  useEffect(() => {
    const dialog = navDialogRef.current;
    if (!dialog) return;
    if (isNavOpen) {
      if (!dialog.open) dialog.showModal();
    } else {
      if (dialog.open) dialog.close();
    }
  }, [isNavOpen]);

  // Click outside to close nav dialog
  useEffect(() => {
    const abortController = new AbortController();
    if (isNavOpen) {
      window.addEventListener(
        "mousedown",
        (event) => {
          if (isNavOpen && navDialogRef.current) {
            const rect = navDialogRef.current.getBoundingClientRect();
            if (
              event.target instanceof Node &&
              navDialogRef.current.open &&
              (event.clientX < rect.left ||
                event.clientX > rect.right ||
                event.clientY < rect.top ||
                event.clientY > rect.bottom)
            ) {
              setNavOpen(false);
            }
          }
        },
        { signal: abortController.signal }
      );
    }
    return () => {
      abortController.abort();
    };
  }, [isNavOpen]);

  // Dialog close event (esc, etc)
  useEffect(() => {
    const navDialog = navDialogRef.current;
    const abortController = new AbortController();
    if (navDialog) {
      navDialog.addEventListener("close", () => setNavOpen(false), {
        signal: abortController.signal
      });
    }
    return () => {
      abortController.abort();
    };
  }, []);

  return (
    <div className="flex">
      <aside className="sticky top-0 hidden h-screen bg-stone-100 p-7 sm:block">
        <nav className="flex flex-col gap-y-4">
          <a
            href="/actors"
            data-active={pageContext.urlPathname === "/actors"}
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
            href="/videos"
            data-active={pageContext.urlPathname === "/videos"}
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
            className="material-symbols-rounded flex size-10 items-center justify-center rounded-full active:bg-stone-100"
            onClick={() => setNavOpen(true)}
          >
            menu
          </button>
        </header>
        <dialog
          ref={navDialogRef}
          className="h-full max-h-full w-full max-w-xs bg-white backdrop:bg-black/30"
        >
          <header className="flex h-16 items-center justify-between px-4">
            <button
              className="material-symbols-rounded flex size-10 items-center justify-center rounded-full active:bg-stone-100"
              onClick={() => setNavOpen(false)}
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
        {props.children}
      </div>
    </div>
  );
}
