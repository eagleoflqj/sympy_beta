<script setup lang="ts">
import { computed } from 'vue'
import { NScrollbar } from 'naive-ui'
import BetaCopyLatexButton from '../BetaCopyLatexButton.vue'

const props = defineProps<{
  content: TexContent
  showCopyButton?: boolean
}>()

const tex = computed(() => {
  return props.content.tex + (props.content.numeric ? '\\approx' + props.content.approximation : '')
})
</script>

<template>
  <div
    v-if="showCopyButton"
    style="text-align: right"
  >
    <beta-copy-latex-button :tex="tex" />
  </div>
  <n-scrollbar x-scrollable>
    <vue-mathjax
      :formula="'$$' + tex + '$$'"
    />
  </n-scrollbar>
</template>
