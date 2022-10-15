<script setup lang="ts">
import { Math } from '@vicons/tabler'
import BetaCopyButton from './BetaCopyButton.vue'

defineProps<{
  tex: string
}>()
</script>

<template>
  <beta-copy-button
    :copied="tex"
    :icon-component="Math"
    popover-text="Copy LaTeX"
  />
</template>
