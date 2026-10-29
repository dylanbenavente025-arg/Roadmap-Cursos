import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// En la máquina local el backend está en localhost:8000.
// Dentro de Docker Compose, API_PROXY_TARGET apunta al servicio "backend".
const apiTarget = process.env.API_PROXY_TARGET ?? 'http://localhost:8000'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      // TRD §3.3: el navegador solo habla con Vite; /api/* se reenvía al backend.
      // xfwd agrega X-Forwarded-For (lo necesita el rate limiting del login).
      '/api': { target: apiTarget, xfwd: true },
    },
  },
})