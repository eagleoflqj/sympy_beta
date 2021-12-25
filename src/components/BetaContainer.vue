<script setup>
import { computed, defineAsyncComponent, toRaw } from 'vue'

const props = defineProps({
  card: {
    type: Object,
    default: () => {}
  },
  callback: {
    type: Object,
    default: () => {}
  }
})

const { card, callback } = toRaw(props)

const cardType = computed(() => defineAsyncComponent(() => import(`./contents/Beta${card.type}.vue`)))
</script>

<template>
  <component
    :is="cardType"
    :card="card"
    :callback="callback"
  />
</template>
