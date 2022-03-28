<script setup>
import BetaCopyTextButton from '@/components/BetaCopyTextButton.vue'

defineProps({
  card: {
    type: Object,
    required: true
  }
})
</script>

<template>
  <div style="text-align: right">
    <beta-copy-text-button :text="card.text" />
  </div>
  {{ card.text }}
</template>
