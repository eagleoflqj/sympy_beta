<script setup lang="ts">
import { NButton } from 'naive-ui'

defineProps<{
  name: string
  callback: () => void
}>()
</script>

<template>
  <div class="card_options">
    <n-button
      secondary
      type="primary"
      @click="callback"
    >
      {{ name }}
    </n-button>
  </div>
</template>
