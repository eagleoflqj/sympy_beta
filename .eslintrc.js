module.exports = {
  env: {
    browser: true,
    es2021: true,
    worker: true
  },
  extends: [
    'plugin:vue/vue3-recommended',
    'standard'
  ],
  parserOptions: {
    ecmaVersion: 'latest',
    parser: '@typescript-eslint/parser',
    sourceType: 'module'
  },
  plugins: [
    'vue',
    '@typescript-eslint'
  ],
  globals: {
    loadPyodide: true,
    d3: true
  },
  rules: {
    'func-call-spacing': 0,
    "@typescript-eslint/no-unused-vars": "error",
    "no-undef": 0,
    "no-use-before-define": 0,
    "@typescript-eslint/no-use-before-define": "error",
    'vue/require-v-for-key': 0,
    'vue/valid-v-for': 0,
    'vue/no-v-html': 0
  }
}
