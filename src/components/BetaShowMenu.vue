<script setup>
import { NIcon, NPopover } from 'naive-ui'
import { Menu2 } from '@vicons/tabler'

</script>

<template>
  <n-popover>
    <template #trigger>
      <n-icon
        :component="Menu2"
        style="padding-right: 10px"
      />
    </template>
    <slot />
  </n-popover>
</template>
