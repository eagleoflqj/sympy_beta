<script setup lang="ts">
import { computed } from 'vue'
import { Markdown } from '@vicons/fa'
import BetaCopyButton from './BetaCopyButton.vue'
// @ts-ignore
import escapeMarkdown from 'markdown-escape'

const props = defineProps<{
  thead: string[]
  tbody: (string | TexContent)[][]
}>()

function escape (textOrTex: string | TexContent) {
  if (typeof textOrTex === 'string') {
    return escapeMarkdown(textOrTex).replace(/\|/g, '\\|')
  }
  return '$' + textOrTex.tex + '$'
}

function arrayToMarkdown (array: (string | TexContent)[]) {
  return array.map(escape).join('|')
}

const markdownText = computed(() => {
  const markDownLines = [arrayToMarkdown(props.thead), Array(props.thead.length).fill('-').join('|')]
  markDownLines.push(...props.tbody.map(arrayToMarkdown))
  markDownLines.push('')
  return markDownLines.join('\n')
})
</script>

<template>
  <beta-copy-button
    :copied="markdownText"
    :icon-component="Markdown"
    popover-text="Copy Markdown"
  />
</template>
