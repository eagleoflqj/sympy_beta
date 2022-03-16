<script setup>
import { computed } from 'vue'
import { NScrollbar } from 'naive-ui'
import BetaCopyLatexButton from '@/components/BetaCopyLatexButton.vue'

const props = defineProps({
  card: {
    type: Object,
    required: true
  }
})

const tex = computed(() => {
  return props.card.tex + (props.card.numeric ? '\\approx' + props.card.approximation : '')
})
</script>

<template>
  <div style="text-align: right">
    <beta-copy-latex-button :tex="tex" />
  </div>
  <n-scrollbar x-scrollable>
    <vue-mathjax
      :formula="'$$' + tex + '$$'"
    />
  </n-scrollbar>
</template>
