import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
    server: {
    host: true, // Exposes the app to external networks
    port: process.env.PORT || 3000,
    }
})
