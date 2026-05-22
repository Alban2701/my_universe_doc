import path from "node:path";
import tailwindcss from "@tailwindcss/vite";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

// https://vite.dev/config/
export default defineConfig({
	plugins: [react(), tailwindcss()],
	resolve: {
		alias: {
			"@my_types": path.resolve(__dirname, "./src/types"),
			"@components": path.resolve(__dirname, "./src/components"),
			"@panels": path.resolve(__dirname, "./src/components/UI/Panels"),
			"@": path.resolve(__dirname, "./")
		},
	},
	server: {
		proxy: {
			"/api": {
				target: "http://localhost:8000/",
				changeOrigin: true,
				rewrite: (path) => path.replace(/^\/api/, ""),
			},
		},
	},
});
