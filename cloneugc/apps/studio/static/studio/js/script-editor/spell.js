import { Mark, mergeAttributes } from "@tiptap/core";
import Text from "@tiptap/extension-text";

const Spell = Mark.create({
  name: "spell",
  exitable: true,
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
  addKeyboardShortcuts() {
    return {
      "Mod-Shift-s": () => this.editor.commands.toggleMark(this.name),
    };
  },
});

export const ScriptText = Text.extend({
  renderText({ node }) {
    const hasSpellMark = node.marks.some((mark) => mark.type.name === "spell");

    return hasSpellMark ? `<spell>${node.text}</spell>` : node.text;
  },
});

export default Spell;
