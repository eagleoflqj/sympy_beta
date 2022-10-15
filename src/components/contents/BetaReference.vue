<script setup lang="ts">
import { NA } from 'naive-ui'

defineProps<{
  content: ReferenceContent
}>()
</script>

<template>
  <ul>
    <li v-for="link in content.links">
      <n-a
        :href="link"
        target="_blank"
      >
        {{ link }}
      </n-a>
    </li>
  </ul>
</template>
