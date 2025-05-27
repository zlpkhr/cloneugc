const icons = [
  "comedy_mask",
  "movie",
  "menu",
  "menu_open",
  "close",
  "play_arrow",
  "pause",
  "download"
].toSorted((a, b) => a.localeCompare(b));

export default function Head() {
  return (
    <>
      <link rel="preconnect" href="https://fonts.googleapis.com" />
      <link
        rel="preconnect"
        href="https://fonts.gstatic.com"
        crossOrigin="anonymous"
      />
      <link
        href="https://fonts.googleapis.com/css2?family=Commissioner:wght@400..700&display=swap"
        rel="stylesheet"
      />
      <link
        rel="stylesheet"
        href={`https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..24,600,1,0&icon_names=${icons.join(",")}`}
      />
    </>
  );
}
