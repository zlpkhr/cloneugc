import {
  Mark,
  mergeAttributes,
} from "https://cdn.jsdelivr.net/npm/@tiptap/core@2.12.0/+esm";

const Spell = Mark.create({
  name: "spell",
  parseHTML() {
    return [
      {
        tag: `span[data-type="${this.name}"]`,
      },
    ];
  },
  renderHTML({ HTMLAttributes }) {
    return [
      "span",
      mergeAttributes(HTMLAttributes, {
        "data-type": this.name,
        class: "rounded-sm bg-yellow-200 px-px font-medium text-black",
      }),
      0,
    ];
  },
  addCommands() {
    return {
      toggleSpell:
        () =>
        ({ commands }) => {
          return commands.toggleMark(this.name);
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
