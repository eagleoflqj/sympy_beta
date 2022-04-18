<script setup>
import { ref, watchEffect } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { NInputGroup, NInput, NButton, NH1, NPopover } from 'naive-ui'

const input = ref()
const router = useRouter()
function submit () {
  if (input.value) {
    router.push({ name: 'Result', params: { expr: input.value } })
  }
}

const route = useRoute()
watchEffect(() => {
  input.value = route.params.expr || ''
})
</script>

<template>
  <div
    class="input"
  >
    <n-h1>
      <router-link :to="'/'">
        <img
          src="/favicon.svg"
          alt=""
        >
        SymPy Beta
      </router-link>
    </n-h1>
    <n-input-group style="width: calc(100vw - 24px); max-width: 584px; margin: auto">
      <n-input
        v-model:value="input"
        type="text"
        placeholder
        clearable
        style="font-family: 'Droid Sans Mono', monospace"
        @keyup.enter="submit"
      />
      <n-popover>
        <template #trigger>
          <n-button
            type="primary"
            @click="submit"
          >
            =
          </n-button>
        </template>
        compute input
      </n-popover>
    </n-input-group>
  </div>
</template>

<style scoped>
h1 {
  margin-bottom: 0;
  text-align: center;
}

h1 a {
  color: #fff;
  text-decoration: none;
}

h1 a img {
  vertical-align: middle;
}

img {
  height: 75px
}

.input {
  padding-bottom: 20px;
  background: #3b5526;
  display: flex;
  flex-direction: column;
}
</style>
