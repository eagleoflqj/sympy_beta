<script setup lang="ts">
import { ref, computed, toRaw } from 'vue'
import { NSpace, NSwitch, NIcon, NEquation } from 'naive-ui'
import { LinearScaleFilled, DivideFilled } from '@vicons/material'
import BetaCopyLatexButton from '../BetaCopyLatexButton.vue'

const props = defineProps<{
  content: ContinuedFractionContent
}>()

const { n, finite, repeated } = toRaw(props.content)

function constructLinear () {
  let tail = !repeated ? '\\cdots' : repeated.length > 0 ? `\\overline{${repeated.join()}}` : ''
  if (finite.length > 0 && tail !== '') {
    tail = `,${tail}`
  }
  return `[${n};${finite.join()}${tail}]`
}

function constructFraction () {
  const middle = [...finite]
  let tail = !repeated || repeated.length ? '+\\cdots' : ''
  if (repeated && repeated.length > 0) {
    middle.push(...repeated)
    if (repeated.length <= 5) {
      middle.push(...repeated)
    }
  }
  let i = middle.length
  while (i--) {
    tail = `+\\frac{1}{${middle[i]}${tail}}`
  }
  return n === 0 ? tail.substring(1) : `${n}${tail}`
}

const linearForm = constructLinear()
const fractionForm = constructFraction()

const fraction = ref(false)
const tex = computed(() => fraction.value ? fractionForm : linearForm)
</script>

<template>
  <n-space vertical>
    <div style="display: flex; justify-content: space-between">
      <n-switch v-model:value="fraction">
        <template #checked>
          fraction
        </template>
        <template #checked-icon>
          <n-icon :component="DivideFilled" />
        </template>
        <template #unchecked-icon>
          <n-icon :component="LinearScaleFilled" />
        </template>
        <template #unchecked>
          linear
        </template>
      </n-switch>
      <beta-copy-latex-button :tex="tex" />
    </div>
    <n-equation
      :value="tex"
    />
  </n-space>
</template>
