<script setup lang="ts">
import { NIcon, NPopover, NA } from 'naive-ui'
import { BrandOpenSource } from '@vicons/tabler'
import { homepage } from '../../package.json'

const props = defineProps<{
  source: string
}>()

const link = `${homepage}/tree/master/kernel/${props.source}`
</script>

<template>
  <n-popover>
    <template #trigger>
      <n-a
        :href="link"
        target="_blank"
      >
        <n-icon
          :component="BrandOpenSource"
          size="32"
        />
      </n-a>
    </template>
    See source on GitHub
  </n-popover>
</template>
