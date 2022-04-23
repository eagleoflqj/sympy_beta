import { resolve } from 'path'
import { execSync } from 'child_process'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import pluginRewriteAll from 'vite-plugin-rewrite-all';
import { VitePWA } from 'vite-plugin-pwa'
import replace from '@rollup/plugin-replace'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    replace({
      __COMMIT__: execSync('git rev-parse HEAD').toString().trim(),
      __BUILD_DATE__: new Date().toLocaleString()
    }),
    vue(),
    pluginRewriteAll(),
    VitePWA({
      registerType: 'autoUpdate',
      includeAssets: ['*.whl'],
      manifest: {
        name: 'SymPy Beta',
        short_name: 'SymPy Beta',
        'icons': [
          {
            src: 'favicon.svg',
            sizes: 'any',
            type: 'image/svg+xml',
            purpose: 'any maskable',
          }
        ]
      }
    })
  ],
  resolve: {
    alias: {
      '@': resolve(__dirname, './src'),
    },
  }
})
