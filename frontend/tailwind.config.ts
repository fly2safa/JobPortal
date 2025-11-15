import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./features/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: 'class', // Enable dark mode with class strategy
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#075299',
          50: '#E6F0F9',
          100: '#CCE1F3',
          200: '#99C3E7',
          300: '#66A5DB',
          400: '#3387CF',
          500: '#075299',
          600: '#06427A',
          700: '#04315B',
          800: '#03213D',
          900: '#01101E',
        },
        // Dark mode specific colors
        dark: {
          bg: {
            primary: '#0f172a',    // slate-900
            secondary: '#1e293b',  // slate-800
            tertiary: '#334155',   // slate-700
          },
          text: {
            primary: '#f1f5f9',    // slate-100
            secondary: '#cbd5e1',  // slate-300
            tertiary: '#94a3b8',   // slate-400
          },
          border: '#475569',       // slate-600
        },
      },
    },
  },
  plugins: [],
};
export default config;

