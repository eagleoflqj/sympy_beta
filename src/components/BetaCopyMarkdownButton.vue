<script setup>
import { computed } from 'vue'
import { Markdown } from '@vicons/fa'
import BetaCopyButton from '@/components/BetaCopyButton.vue'
import escapeMarkdown from 'markdown-escape'

const props = defineProps({
  thead: {
    type: Array,
    required: true
  },
  tbody: {
    type: Array,
    required: true
  }
})

const markdownText = computed(() => {
  const markDownLines = [arrayToMarkdown(props.thead), Array(props.thead.length).fill('-').join('|')]
  markDownLines.push(...props.tbody.map(arrayToMarkdown))
  markDownLines.push('')
  return markDownLines.join('\n')
})

function escape (text) {
  return escapeMarkdown(text).replace('|', '\\|')
}

function arrayToMarkdown (array) {
  return array.map(escape).join('|')
}

</script>

<template>
  <beta-copy-button
    :copied="markdownText"
    :icon-component="Markdown"
    popover-text="Copy Markdown"
  />
</template>
