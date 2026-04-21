/**@type {import('tailwindcss').Config}*/
module.exports = {

  content: [ './anapiApp/templates/**/*.html',
  './anapiApp/**/*.py',
  './anapiApp/static/src/**/*.css',
  ],
  
  theme: {
    extend: {
      colors: {
        jaune: '#FFBE03',
          vert: '#107C41',
          bleu: '#025D7E',
          'bleu-clair': '#00ADEE',
      },
    },
  },

  plugins: [],
}