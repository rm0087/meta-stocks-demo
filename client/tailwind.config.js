/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.js"],
  theme: {
    extend: {
      fontFamily: {
        newsCycle: ['newscycle-regular','sans-serif'],
        roboto: ['Roboto', 'sans-serif'],
        chivo: ['Chivo', 'sans-serif'],
        sanscaption: ['PT Sans Caption', 'sans-serif'],
        leaguegothic: ['League Gothic', 'sans-serif']
      },
    },
  },
  plugins: [],
};

