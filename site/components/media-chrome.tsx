import { clientOnly } from "vike-react/clientOnly";

export const MediaControlBar = clientOnly(() =>
  import("media-chrome/react").then((m) => m.MediaControlBar)
);
export const MediaController = clientOnly(() =>
  import("media-chrome/react").then((m) => m.MediaController)
);

export const MediaPlayButton = clientOnly(() =>
  import("media-chrome/react").then((m) => m.MediaPlayButton)
);
