<script setup lang="ts">
import { computed, defineAsyncComponent } from 'vue'

const props = defineProps<{
  content: Content
  callback?: {}
}>()

const cardType = computed(() => defineAsyncComponent(() => import(`./contents/Beta${props.content.type}.vue`)))
</script>

<template>
  <component
    :is="cardType"
    :content="content"
    :callback="callback"
  />
</template>
