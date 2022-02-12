module.exports = {
    "env": {
        "browser": true,
        "es2021": true,
        "worker": true,
        "vue/setup-compiler-macros": true
    },
    "extends": [
        "plugin:vue/vue3-recommended",
        "standard"
    ],
    "parserOptions": {
        "ecmaVersion": 13,
        "sourceType": "module"
    },
    "plugins": [
        "vue"
    ],
    "globals": {
        "loadPyodide": true,
        "d3": true
    },
    "rules": {
        "vue/require-v-for-key": 0,
        "vue/valid-v-for": 0,
        "vue/no-v-html": 0
    }
};
