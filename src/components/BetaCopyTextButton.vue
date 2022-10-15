<script setup lang="ts">
import { Copy } from '@vicons/tabler'
import BetaCopyButton from './BetaCopyButton.vue'

defineProps<{
  text: string
}>()
</script>

<template>
  <beta-copy-button
    :copied="text"
    :icon-component="Copy"
    popover-text="Copy text"
  />
</template>
