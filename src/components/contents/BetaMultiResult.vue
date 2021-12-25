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
    <li v-for="result in card.results">
      <div class="cell_input">
        {{ result.input }}
      </div>
      <beta-container :card="result.output" />
    </li>
  </ul>
</template>
