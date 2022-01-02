<script setup>
import { NCode } from 'naive-ui'
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
      <n-code
        :code="result.input"
        language="python"
        inline
      />
      <beta-container :card="result.output" />
    </li>
  </ul>
</template>
