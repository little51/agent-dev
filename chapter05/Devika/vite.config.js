import { sveltekit } from "@sveltejs/kit/vite";
import { defineConfig } from "vite";
import wasm from "vite-plugin-wasm";

export default defineConfig({
  plugins: [sveltekit(), wasm()],
  server: {
    port: 3000
  },
  preview: {
    host: '0.0.0.0', 
    port: 3001,
    proxy: {
      '/api': { 
        target: 'http://172.16.62.37:1337/api',
        changeOrigin: true
      },
      '/socket.io': {
        target: 'ws://172.16.62.37:1337',
        ws: true
      }
   }
  },
  build: {
    target: "esnext",
  },
});
