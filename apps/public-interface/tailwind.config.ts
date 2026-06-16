import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./content/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        earth: {
          green: "#2f4538",
          deep: "#1b271f",
          sand: "#d8c8a8",
          sandlight: "#f3ecdd",
          charcoal: "#262522",
          gold: "#b8893b",
          goldmuted: "#9a7636",
        },
      },
      fontFamily: {
        sans: ["ui-sans-serif", "system-ui", "Segoe UI", "Roboto", "sans-serif"],
        serif: ["ui-serif", "Georgia", "serif"],
      },
      maxWidth: { prose: "70ch" },
    },
  },
  plugins: [],
};
export default config;
