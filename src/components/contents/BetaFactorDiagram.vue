<script setup>
import { ref, toRaw, onMounted } from 'vue'
import { NA } from 'naive-ui'
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
  <div
    style="text-align: center"
  >
    <svg ref="container" />
  </div>
  <n-a
    href="https://mathlesstraveled.com/2012/10/05/factorization-diagrams/"
    target="_blank"
  >
    About this diagram
  </n-a>
</template>
