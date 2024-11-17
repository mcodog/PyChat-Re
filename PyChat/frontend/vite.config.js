import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0', // or a specific IP like '127.0.0.1'
    port: 3000 // Replace with your desired port
  }
})
