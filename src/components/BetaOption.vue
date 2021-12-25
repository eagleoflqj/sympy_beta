<script setup>
import { NButton } from 'naive-ui'

defineProps({
  name: {
    type: String,
    default: () => ''
  },
  callback: {
    type: Function,
    default: () => () => {}
  }
})
</script>

<template>
  <div class="card_options">
    <n-button
      type="primary"
      @click="callback"
    >
      {{ name }}
    </n-button>
  </div>
</template>
