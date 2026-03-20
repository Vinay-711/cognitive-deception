/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}",
    "./pages/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
    "./views/**/*.{js,ts,jsx,tsx}",
    "./hooks/**/*.{js,ts,jsx,tsx}",
    "./services/**/*.{js,ts,jsx,tsx}",
    "./visualizations/**/*.{js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {
      colors: {
        cyber: {
          bg: "#05070A",
          panel: "#0B0F14",
          accent: "#00E5FF",
          alert: "#FF3B3B",
          purple: "#7C4DFF"
        }
      },
      fontFamily: {
        body: ["Inter", "IBM Plex Sans", "ui-sans-serif", "system-ui", "sans-serif"],
        mono: ["IBM Plex Mono", "ui-monospace", "SFMono-Regular", "monospace"]
      },
      boxShadow: {
        neon: "0 0 0 1px rgba(0,229,255,.3), 0 0 40px rgba(0,229,255,.12)",
        danger: "0 0 0 1px rgba(255,59,59,.3), 0 0 30px rgba(255,59,59,.15)"
      },
      backgroundImage: {
        grid: "radial-gradient(circle at 1px 1px, rgba(0,229,255,0.12) 1px, transparent 0)"
      }
    }
  },
  plugins: []
};
