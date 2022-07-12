<script setup>
import { Math } from '@vicons/tabler'
import BetaCopyButton from '@/components/BetaCopyButton.vue'

defineProps({
  tex: {
    type: String,
    required: true
  }
})
</script>

<template>
  <beta-copy-button
    :copied="tex"
    :icon-component="Math"
    popover-text="Copy LaTeX"
  />
</template>
