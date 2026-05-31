/** @type {import('tailwindcss').Config} */
export default {
  content: [],
  theme: {
    extend: {
      colors: {
        ink: {
          DEFAULT: '#0a0a0a',
          soft: '#141414',
          muted: '#1f1f1f',
        },
        chalk: {
          DEFAULT: '#f5f2ea',
          dark: '#e8e4da',
        },
        acid: {
          DEFAULT: '#d4ff00',
          dim: '#b8e600',
        },
        smoke: {
          DEFAULT: '#8a8a8a',
          light: '#b3b3b3',
        },
      },
      fontFamily: {
        sans: ['Space Grotesk', 'system-ui', 'sans-serif'],
        display: ['Bebas Neue', 'Impact', 'sans-serif'],
      },
      boxShadow: {
        hard: '4px 4px 0 0 #0a0a0a',
        acid: '4px 4px 0 0 #d4ff00',
      },
      letterSpacing: {
        street: '0.12em',
      },
    },
  },
  plugins: [],
}
