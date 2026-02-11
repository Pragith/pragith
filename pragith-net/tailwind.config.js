/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/templates/**/*.html"],
  darkMode: 'class',
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        display: ['DM Sans', 'Inter', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      colors: {
        accent: '#E8590C',
        // Semantic colors that auto-switch via CSS variables
        ink: 'rgb(var(--color-ink) / <alpha-value>)',
        page: 'rgb(var(--color-page) / <alpha-value>)',
        surface: 'rgb(var(--color-surface) / <alpha-value>)',
        line: 'rgb(var(--color-line) / <alpha-value>)',
      },
    },
  },
  plugins: [],
}
