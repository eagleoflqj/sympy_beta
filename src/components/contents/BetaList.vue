<script setup>
import BetaContainer from '@/components/BetaContainer.vue'

defineProps({
  card: {
    type: Object,
    default: () => {}
  }
})
</script>

<template>
  <ul>
    <li v-for="item in card.list">
      <beta-container :card="item" />
    </li>
  </ul>
</template>
