import { nodeResolve } from '@rollup/plugin-node-resolve'
import esbuild from 'rollup-plugin-esbuild'
import json from '@rollup/plugin-json'

const isProd = process.env.NODE_ENV === 'production'

export default ['src/pyodideWorker.ts', 'src/shellWorker.ts'].map(input => ({
  input,
  output: {
    dir: 'public',
    sourcemap: !isProd,
    format: 'iife'
  },
  plugins: [
    nodeResolve(),
    json(),
    esbuild({
      sourceMap: !isProd,
      minify: isProd
    })
  ]
}))
