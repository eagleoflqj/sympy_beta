<script setup>
import { NIcon, NPopover, NButton } from 'naive-ui'
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
        <a
          :href="img ? img.src : '#'"
          :download="name"
        >
          <n-icon
            :component="Image"
            size="32"
          />
        </a>
      </n-button>
    </template>
    Download SVG
  </n-popover>
</template>
