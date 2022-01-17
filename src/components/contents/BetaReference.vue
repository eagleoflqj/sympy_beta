<script setup>
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
      <a
        :href="link"
        target="_blank"
      >{{ link }}</a>
    </li>
  </ul>
</template>
