import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./modules/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // KASAMOR earth palette
        earth: {
          green: "#2f4538",
          deep: "#1f2d24",
          sand: "#d8c8a8",
          sandlight: "#efe7d4",
          charcoal: "#2b2b2b",
          gold: "#b8893b",
          goldmuted: "#9a7636",
        },
      },
      fontFamily: {
        sans: ["ui-sans-serif", "system-ui", "Segoe UI", "Roboto", "sans-serif"],
      },
    },
  },
  plugins: [],
};
export default config;
