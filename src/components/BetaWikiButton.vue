<script setup lang="ts">
import { NIcon, NPopover, NA } from 'naive-ui'
import { WikipediaW } from '@vicons/fa'

const props = defineProps<{
  wiki: string
}>()

const link = `https://en.wikipedia.org/wiki/${props.wiki}`
</script>

<template>
  <n-popover>
    <template #trigger>
      <n-a
        :href="link"
        target="_blank"
      >
        <n-icon
          :component="WikipediaW"
          size="32"
        />
      </n-a>
    </template>
    Refer to Wikipedia
  </n-popover>
</template>
