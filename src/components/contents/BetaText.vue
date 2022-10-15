<script setup lang="ts">
import BetaCopyTextButton from '../BetaCopyTextButton.vue'

defineProps<{
  content: TextContent
}>()
</script>

<template>
  <div style="text-align: right">
    <beta-copy-text-button :text="content.text" />
  </div>
  {{ content.text }}
</template>
