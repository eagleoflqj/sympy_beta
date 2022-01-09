<script setup>
import { ref, watchEffect } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { NInputGroup, NInput, NButton, NSpace } from 'naive-ui'

const input = ref()
const router = useRouter()
function submit () {
  if (input.value) {
    router.push({ name: 'Result', params: { expr: input.value } })
  }
}

const route = useRoute()
watchEffect(() => {
  if (typeof route.params.expr === 'undefined') {
    return
  }
  input.value = route.params.expr
})
</script>

<template>
  <n-space
    class="input"
    vertical
  >
    <h1>
      <router-link :to="'/'">
        <img
          src="/src/assets/logo.png"
          alt="SymPy Beta logo"
          width="75"
          height="50"
        >
        SymPy Beta
      </router-link>
    </h1>
    <n-input-group style="width: calc(100vw - 24px); max-width: 584px; margin: auto">
      <n-input
        v-model:value="input"
        type="text"
        placeholder
        clearable
        @keyup.enter="submit"
      />
      <n-button
        type="primary"
        @click="submit"
      >
        =
      </n-button>
    </n-input-group>
  </n-space>
</template>
