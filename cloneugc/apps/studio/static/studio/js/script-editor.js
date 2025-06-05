import { Editor } from "@tiptap/core";
import Document from "@tiptap/extension-document";
import History from "@tiptap/extension-history";
import Paragraph from "@tiptap/extension-paragraph";
import Text from "@tiptap/extension-text";
import Break from "studio/script-editor/break";
import Spell from "studio/script-editor/spell";

new Editor({
  element: document.querySelector("#script-editor"),
  extensions: [Document, Text, Paragraph, Break, Spell, History],
  editorProps: {
    attributes: {
      class:
        "bg-white border border-black/20 rounded-md text-lg font-medium p-3 focus:outline-pink-700 content-noneditable:bg-stone-100 content-noneditable:text-stone-500",
    },
  },
  onUpdate: ({ editor }) => {
    console.log(editor.getHTML());
  },
});
