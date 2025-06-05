import { Node, mergeAttributes } from "@tiptap/core";

const Break = Node.create({
  name: "break",
  inline: true,
  group: "inline",
  atom: true,
  addAttributes() {
    return {
      duration: {
        renderHTML(attributes) {
          return {
            "data-duration": attributes.duration,
          };
        },
        parseHTML(element) {
          return parseFloat(element.getAttribute("data-duration"));
        },
      },
    };
  },
  renderHTML({ HTMLAttributes, node }) {
    return [
      "span",
      mergeAttributes(HTMLAttributes, {
        "data-type": this.name,
        class:
          "rounded-sm bg-stone-100 px-px font-medium text-black outline-1 outline-black/20 tp-node-selected:outline-2 tp-node-selected:outline-pink-800",
      }),
      formatDuration(node.attrs.duration),
    ];
  },
  parseHTML() {
    return [
      {
        tag: `span[data-type="${this.name}"]`,
      },
    ];
  },
  renderText({ node }) {
    return `<break time="${toTime(node.attrs.duration)}" />`;
  },
  addCommands() {
    return {
      insertBreak:
        (duration) =>
        ({ commands }) => {
          return commands.insertContent({
            type: this.name,
            attrs: { duration },
          });
        },
    };
  },
  addKeyboardShortcuts() {
    return {
      "Mod-Shift-b": () => {
        const input = prompt("Break duration (0.1 to 10 seconds):", "1");

        if (!input) {
          return true; // Prevent browser's default shortcut
        }

        const duration = parseFloat(input.trim());

        if (!isValidDuration(duration)) {
          alert("Invalid duration.");
          return true;
        }

        this.editor.commands.insertBreak(duration);
        return true;
      },
    };
  },
});

export default Break;

function isValidDuration(value) {
  if (isNaN(value)) {
    return false;
  }

  if (value < 0) {
    return false;
  }

  if (value > 10) {
    return false;
  }

  return true;
}

function formatDuration(value) {
  if (Number.isInteger(value)) {
    return value + "s";
  }

  return value.toFixed(1) + "s";
}

function toTime(duration) {
  if (duration < 1) {
    return Math.round(duration * 1000) + "ms";
  }

  return Math.round(duration) + "s";
}
