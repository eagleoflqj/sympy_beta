<script setup lang="ts">
import BetaContainer from '../BetaContainer.vue'

defineProps<{
  content: ListContent
}>()

</script>

<template>
  <ul>
    <li v-for="item in content.list">
      <beta-container :content="item" />
    </li>
  </ul>
</template>
