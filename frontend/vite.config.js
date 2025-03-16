import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
        configure: (proxy, _options) => {
          proxy.on('error', (err, _req, _res) => {
            console.log('プロキシエラー:', err);
          });
          proxy.on('proxyReq', (_proxyReq, req, _res) => {
            console.log('リクエスト送信:', req.method, req.url);
          });
          proxy.on('proxyRes', (proxyRes, req, _res) => {
            console.log('レスポンス受信:', proxyRes.statusCode, req.url);
          });
        },
      }
    }
  },
})
