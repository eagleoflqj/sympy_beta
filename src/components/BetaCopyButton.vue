<script setup lang="ts">
import { Component } from 'vue'
import { NIcon, NPopover, NButton, useMessage } from 'naive-ui'

const props = defineProps<{
  copied: string
  iconComponent: Component
  popoverText: string
}>()

const message = useMessage()

function handleClick () {
  navigator.clipboard.writeText(props.copied).then(() => {
    message.success('Copied to Clipboard')
  })
}
</script>

<template>
  <n-popover>
    <template #trigger>
      <n-button
        text
        @click="handleClick"
      >
        <n-icon
          :component="iconComponent"
          size="32"
        />
      </n-button>
    </template>
    {{ popoverText }}
  </n-popover>
</template>
