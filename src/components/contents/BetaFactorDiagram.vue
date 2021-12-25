<script setup>
import { ref, toRaw, onMounted } from 'vue'
import { FactorDiagram } from '@/js/factordiagram.js'

const props = defineProps({
  card: {
    type: Object,
    default: () => { }
  }
})

const { card } = toRaw(props)

const container = ref(null)

onMounted(() => (new FactorDiagram(card.primes, container.value)).draw())
</script>

<template>
  <div class="factorization-diagram">
    <svg ref="container" />
  </div>
</template>

<style>
/* Factorization diagrams */

.factorization-diagram p {
  text-align: left;
  font-family: "Open Sans", sans-serif;
  font-size: smaller;
  margin: 0;
  padding: 0;
}
</style>
