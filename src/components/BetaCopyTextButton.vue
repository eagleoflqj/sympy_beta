<script setup>
import { Copy } from '@vicons/tabler'
import BetaCopyButton from '@/components/BetaCopyButton.vue'

defineProps({
  text: {
    type: String,
    required: true
  }
})
</script>

<template>
  <beta-copy-button
    :copied="text"
    :icon-component="Copy"
    popover-text="Copy text"
  />
</template>
