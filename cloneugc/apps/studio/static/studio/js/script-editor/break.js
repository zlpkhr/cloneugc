import {
  mergeAttributes,
  Node,
} from "https://cdn.jsdelivr.net/npm/@tiptap/core@2.12.0/+esm";

function parseTime(value) {
  if (typeof value !== "string") {
    throw new Error("Time value must be a string.");
  }

  const match = value.match(/^(\d+)(ms|s)$/);

  if (!match) {
    throw new Error("Invalid time value.");
  }

  const number = parseFloat(match.at(1));
  const unit = match.at(2);

  if (isNaN(number)) {
    throw new Error("Invalid time value.");
  }

  if (unit === "ms") {
    return number / 1000;
  }

  return number;
}

function serializeTime(time) {
  if (time < 1) {
    return Math.round(time * 1000) + "ms";
  }

  return Math.round(time) + "s";
}

function isValidTime(time) {
  if (isNaN(time)) {
    return false;
  }

  if (time < 0) {
    return false;
  }

  if (time > 10) {
    return false;
  }

  return true;
}

function formatTime(time) {
  if (Number.isInteger(time)) {
    return time + "s";
  }

  return time.toFixed(1) + "s";
}

const Break = Node.create({
  name: "break",
  group: "inline",
  inline: true,
  atom: true,
  addAttributes() {
    return {
      time: {
        parseHTML: (element) => parseTime(element.getAttribute("data-time")),
        renderHTML: (attributes) => {
          return {
            "data-time": serializeTime(attributes.time),
          };
        },
      },
    };
  },
  parseHTML() {
    return [
      {
        tag: `span[data-type="${this.name}"]`,
      },
    ];
  },
  renderHTML({ node, HTMLAttributes }) {
    return [
      "span",
      mergeAttributes(HTMLAttributes, {
        "data-type": this.name,
        class:
          "rounded-sm bg-stone-100 px-px font-medium text-black outline-1 outline-black/20",
      }),
      formatTime(node.attrs.time),
    ];
  },
  renderText({ node }) {
    return `<break time="${serializeTime(node.attrs.time)}" />`;
  },
  addCommands() {
    return {
      insertBreak:
        (time) =>
        ({ commands }) => {
          return commands.insertContent({
            type: this.name,
            attrs: { time },
          });
        },
    };
  },
  addKeyboardShortcuts() {
    return {
      "Mod-Shift-b": () => {
        const input = prompt("Break duration (0.1 to 10):", "1");

        if (!input) {
          return true; // Prevent browser's default shortcut
        }

        const time = parseFloat(input.trim());

        if (!isValidTime(time)) {
          alert("Invalid time value.");
          return true;
        }

        this.editor.commands.insertBreak(time);
        return true;
      },
    };
  },
});

export default Break;
