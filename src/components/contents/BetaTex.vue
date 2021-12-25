<script setup>
defineProps({
  card: {
    type: Object,
    default: () => {}
  }
})
</script>

<template>
  <vue-mathjax
    :formula="'$$' + card.tex + (card.numeric ? '\\approx' + card.approximation : '') + '$$'"
  />
</template>
