import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        sharda: {
          dark: "#1B2C39",
          navy: "#23394c",
          gold: "#EAA914",
          goldHover: "#D6950B",
          red: "#A61C24",
          redHover: "#8C141B",
          blue: "#0284c7",
          lightBg: "#F8FAFC",
          cardBg: "#FFFFFF",
          border: "#E2E8F0",
        },
      },
      fontFamily: {
        sans: ["Inter", "-apple-system", "BlinkMacSystemFont", "Segoe UI", "Roboto", "sans-serif"],
      },
      boxShadow: {
        sharda: "0 4px 20px -2px rgba(27, 44, 57, 0.08)",
        glass: "0 8px 32px 0 rgba(27, 44, 57, 0.37)",
      }
    },
  },
  plugins: [],
};
export default config;
