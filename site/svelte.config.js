import adapter from "@sveltejs/adapter-auto";
import { vitePreprocess } from "@sveltejs/vite-plugin-svelte";

/** @type {import('@sveltejs/kit').Config} */
const svelteConfig = {
  preprocess: vitePreprocess(),
  kit: {
    adapter: adapter()
  }
};

export default svelteConfig;
