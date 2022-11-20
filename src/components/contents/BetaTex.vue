<script setup lang="ts">
import { computed } from 'vue'
import { NScrollbar, NEquation } from 'naive-ui'
import BetaCopyLatexButton from '../BetaCopyLatexButton.vue'

interface Props {
  content: TexContent
  showCopyButton?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  showCopyButton: true
})

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
    <n-equation
      :value="tex"
      :katex-options="{displayMode: true}"
    />
  </n-scrollbar>
</template>
