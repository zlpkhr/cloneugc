import { Editor } from "https://cdn.jsdelivr.net/npm/@tiptap/core@2.12.0/+esm";
import Document from "https://cdn.jsdelivr.net/npm/@tiptap/extension-document@2.12.0/+esm";
import History from "https://cdn.jsdelivr.net/npm/@tiptap/extension-history@2.12.0/+esm";
import Paragraph from "https://cdn.jsdelivr.net/npm/@tiptap/extension-paragraph@2.12.0/+esm";
import Text from "https://cdn.jsdelivr.net/npm/@tiptap/extension-text@2.12.0/+esm";
import Break from "studio/script-editor/break";
import Spell from "studio/script-editor/spell";

new Editor({
  element: document.querySelector("#script-editor"),
  extensions: [Document, Paragraph, Text, Break, Spell, History],
  content:
    '<p>Start typing your script here... Use <span data-type="spell">Cmd+Shift+S</span> for spell mode and <span data-type="break" data-duration="0.5">0.5s</span> Cmd+Shift+B for breaks.</p>',
  onCreate: ({ editor }) => {
    const textarea = document.querySelector("#script");
    textarea.value = editor.getText();
  },
  onUpdate: ({ editor }) => {
    console.log(editor.getHTML())
    const textarea = document.querySelector("#script");
    textarea.value = editor.getText();
  },
});
