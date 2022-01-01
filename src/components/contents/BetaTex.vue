<script setup>
import { NScrollbar } from 'naive-ui'

defineProps({
  card: {
    type: Object,
    default: () => {}
  }
})
</script>

<template>
  <n-scrollbar x-scrollable>
    <vue-mathjax
      :formula="'$$' + card.tex + (card.numeric ? '\\approx' + card.approximation : '') + '$$'"
    />
  </n-scrollbar>
</template>
