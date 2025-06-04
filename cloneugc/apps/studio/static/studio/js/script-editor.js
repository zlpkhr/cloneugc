import {
  Editor,
  Mark,
  mergeAttributes
} from "https://cdn.jsdelivr.net/npm/@tiptap/core@2.12.0/+esm";
import Document from "https://cdn.jsdelivr.net/npm/@tiptap/extension-document@2.12.0/+esm";
import History from "https://cdn.jsdelivr.net/npm/@tiptap/extension-history@2.12.0/+esm";
import Paragraph from "https://cdn.jsdelivr.net/npm/@tiptap/extension-paragraph@2.12.0/+esm";
import Text from "https://cdn.jsdelivr.net/npm/@tiptap/extension-text@2.12.0/+esm";
import Break from "studio/script-editor/break";


// Custom Spell Mark
const Spell = Mark.create({
  name: "spell",

  parseHTML() {
    return [
      {
        tag: "spell",
      },
    ];
  },

  renderHTML({ HTMLAttributes }) {
    return [
      "spell",
      mergeAttributes(HTMLAttributes, {
        class:
          "bg-yellow-100 font-mono tracking-wider px-1 py-0.5 rounded font-medium",
        "data-spell": "true",
      }),
      0,
    ];
  },

  addCommands() {
    return {
      setSpell:
        () =>
        ({ commands }) => {
          return commands.setMark(this.name);
        },
      toggleSpell:
        () =>
        ({ commands }) => {
          return commands.toggleMark(this.name);
        },
      unsetSpell:
        () =>
        ({ commands }) => {
          return commands.unsetMark(this.name);
        },
    };
  },

  addKeyboardShortcuts() {
    return {
      "Mod-Shift-s": () => this.editor.commands.toggleSpell(),
    };
  },
});

// Initialize editor
const editorElement = document.querySelector("#script-editor");
if (editorElement) {
  // Apply editor styling directly to the element
  editorElement.className =
    "border border-gray-200 rounded-md min-h-48 p-3 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100";

  // Create editor
  const editor = new Editor({
    element: editorElement,
    extensions: [Document, Paragraph, Text, History, Break, Spell],
    content:
      '<p>Start typing your script here... Use <spell>Cmd+Shift+S</spell> for spell mode and <break time="500ms"></break> Cmd+Shift+B for breaks.</p>',
    onUpdate: ({ editor }) => {
      // Sync with the original textarea if it exists - use text value
      const textarea = document.querySelector("#script");
      if (textarea) {
        textarea.value = editor.getText();
      }
    },
  });

  // Sync initial content from textarea
  const textarea = document.querySelector("#script");
  if (textarea && textarea.value) {
    editor.commands.setContent(textarea.value);
  }
}
