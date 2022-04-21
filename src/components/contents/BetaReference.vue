<script setup>
import { NA } from 'naive-ui'

defineProps({
  card: {
    type: Object,
    default: () => {}
  }
})
</script>

<template>
  <ul>
    <li v-for="link in card.links">
      <n-a
        :href="link"
        target="_blank"
      >
        {{ link }}
      </n-a>
    </li>
  </ul>
</template>
