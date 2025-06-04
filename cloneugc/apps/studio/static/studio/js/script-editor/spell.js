import {
  Mark,
  mergeAttributes
} from "https://cdn.jsdelivr.net/npm/@tiptap/core@2.12.0/+esm";

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

export default Spell;