<script setup>
import { NIcon, NPopover, NButton, useMessage } from 'naive-ui'

const props = defineProps({
  copied: {
    type: String,
    required: true
  },
  iconComponent: {
    type: Object,
    required: true
  },
  popoverText: {
    type: String,
    default: () => ''
  }
})

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
