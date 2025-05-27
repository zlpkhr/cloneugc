import tailwindcss from "@tailwindcss/vite";
import react from "@vitejs/plugin-react";
import vike from "vike/plugin";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [vike(), react(), tailwindcss()],
  server: {
    proxy: {
      "/graphql/": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true
      },
      "/api/actors/create/": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true,
        timeout: 120 * 1000
      }
    }
  }
});
