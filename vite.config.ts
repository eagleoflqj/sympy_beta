import { execSync } from 'child_process'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import pluginRewriteAll from 'vite-plugin-rewrite-all'
import { VitePWA } from 'vite-plugin-pwa'
import { run } from 'vite-plugin-run'
import replace from '@rollup/plugin-replace'


const plugins = [
  replace({
    __COMMIT__: execSync('git rev-parse HEAD').toString().trim(),
    __BUILD_DATE__: new Date().toLocaleString()
  }),
  vue(),
  pluginRewriteAll(),
  VitePWA({
    registerType: 'autoUpdate',
    workbox: {
      maximumFileSizeToCacheInBytes: 10000000
    },
    includeAssets: ['*.whl', '*.zip', 'fonts/*.woff2'],
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
]

if (process.env.NODE_ENV !== 'production') {
  plugins.push(run([
    {
      name: 'Transpile worker',
      run: ['pnpm run worker'],
      condition: file => file.includes('Worker.ts')
    }
  ]))
}

export default defineConfig({
  plugins
})
