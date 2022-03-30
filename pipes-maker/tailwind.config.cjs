const config = {
  content: ['./src/**/*.{html,js,svelte,ts}'],

  theme: {
    extend: {
      fontFamily: {
        mono: ['Latin Modern Mono', 'monospace'],
      },
      gridTemplateRows: {
        subgrid: 'subgrid'
      },
      gridTemplateColumns: {
        subgrid: 'subgrid'
      }
    },
  },

  plugins: [],
};

module.exports = config;
