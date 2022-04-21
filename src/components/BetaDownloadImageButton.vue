<script setup>
import { NIcon, NPopover, NButton, NA } from 'naive-ui'
import { Image } from '@vicons/fa'

defineProps({
  img: {
    type: HTMLImageElement,
    required: true
  },
  name: {
    type: String,
    required: true
  }
})
</script>

<template>
  <n-popover>
    <template #trigger>
      <n-button
        text
      >
        <n-a
          :href="img ? img.src : '#'"
          :download="name"
        >
          <n-icon
            :component="Image"
            size="32"
          />
        </n-a>
      </n-button>
    </template>
    Download SVG
  </n-popover>
</template>
