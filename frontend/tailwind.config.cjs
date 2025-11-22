module.exports = {
  darkMode: 'class',
  content: [
    './index.html',
    './src/**/*.{ts,tsx,js,jsx}'
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          DEFAULT: '#6366F1',
          dark: '#4F46E5'
        }
      },
      boxShadow: {
        soft: '0 2px 4px -1px rgba(0,0,0,0.08), 0 4px 10px -1px rgba(0,0,0,0.06)'
      }
    }
  },
  plugins: []
}