<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { NInputGroup, NInput, NButton } from 'naive-ui'

const input = ref()
const router = useRouter()
function submit () {
  if (input.value) {
    router.push({ name: 'Result', params: { expr: input.value } })
  }
}
</script>

<template>
  <div class="input">
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
    <n-input-group style="margin-top: 20px; width: 580px">
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
  </div>
</template>
