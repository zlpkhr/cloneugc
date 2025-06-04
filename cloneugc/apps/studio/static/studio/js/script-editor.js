import { Editor } from "https://cdn.jsdelivr.net/npm/@tiptap/core@2.12.0/+esm";
import StarterKit from "https://cdn.jsdelivr.net/npm/@tiptap/starter-kit@2.12.0/+esm";

const editor = new Editor({
  element: document.querySelector("#script-editor"),
  extensions: [StarterKit],
  content: "<p>Hello World!</p>",
});
