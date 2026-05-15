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
        tm: {
          // Colores TodoMovil — estilo autoelectrolab
          bg: "#0f172a",        // Fondo principal oscuro
          card: "#1e293b",      // Fondo de cards
          border: "#334155",    // Bordes
          accent: "#f59e0b",    // Amarillo TodoMovil
          accent2: "#3b82f6",   // Azul secundario
          text: "#f1f5f9",      // Texto principal
          muted: "#94a3b8",     // Texto secundario
          verde: "#22c55e",     // Semáforo verde
          amarillo: "#eab308",  // Semáforo amarillo
          rojo: "#ef4444",      // Semáforo rojo
          no_aplica: "#6b7280", // Semáforo no aplica
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
};

export default config;
