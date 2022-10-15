<script setup lang="ts">
import { ref, reactive, onMounted, toRaw } from 'vue'
import { NButton, NSpace, NSpin, NCard, NCode } from 'naive-ui'
import { Eye, EyeSlash } from '@vicons/fa'
import { evalCard } from '../workerAPI'
import { Plot2D } from '../js/plot.js'
import BetaAmbiguity from './BetaAmbiguity.vue'
import BetaContainer from './BetaContainer.vue'
import BetaOption from './BetaOption.vue'
import BetaSourceButton from './BetaSourceButton.vue'
import BetaWikiButton from './BetaWikiButton.vue'

const props = defineProps<{
  card: InputResult
  input: string
  chooseVariable: (variable: string) => void
}>()

const { card, input } = toRaw(props)

const cardResult = reactive<CardResult | {}>({})

let digits = 15
const numericCallbacks = reactive<(() => void)[]>([])

onMounted(async () => {
  if ('ambiguity' in card || 'error' in card) {
    return
  }
  if ('name' in card) {
    const hasDigits = (card.parameters || []).indexOf('digits') >= 0
    const evaluate = async () => {
      const parameters = hasDigits ? { digits } : {}
      Object.assign(cardResult, await evalCard(card.name, input, card.variable, parameters))
    }
    evaluate()
    if (hasDigits) {
      numericCallbacks.push(evaluate)
    }
  } else {
    const numerics: TexContent[] = []
    if ('output' in card) {
      if ('numeric' in card.output) {
        numerics.push(card.output)
      } else if ('list' in card.output) {
        card.output.list.forEach(item => 'numeric' in item && numerics.push(item))
      }
    }
    numerics.forEach(item => numericCallbacks.push(async () =>
      Object.assign(item, await evalCard('approximator', item.expression, 'x', { digits }))))
  }
})

function moreDigits () {
  digits += 10
  numericCallbacks.forEach(callback => callback())
}

let plot: Plot2D | null = null
const colors = d3.scale.category10()

function getPlot (container: Element) {
  plot = new Plot2D(container, (cardResult as PlotContent).graphs, async (parameters: { xmin: number, xmax: number }) => {
    const { graphs } = await evalCard((card as ContentCard).name, input, (card as ContentCard).variable, parameters)
    return graphs
  })
  return plot
}

const visibility = ref<{ [key: number]: boolean }>({})

function toggleVisibility (index: number, event: MouseEvent) {
  if (plot !== null) {
    // @ts-ignore
    const style = event.currentTarget.style
    if (visibility.value[index] === false) {
      visibility.value[index] = true
      style.opacity = 1
    } else {
      visibility.value[index] = false
      style.opacity = 0.5
    }
    plot.toggle(index)
  }
}

function highlight (index: number, highlight: boolean) {
  if (plot !== null) {
    plot.highlight(index, highlight)
  }
}

const isFullscreen = ref(false)

function toggleFullscreen (event: KeyboardEvent) {
  if (event.type === 'keyup' && event.key !== 'Escape') {
    return
  }
  if (isFullscreen.value) {
    globalThis.removeEventListener('keyup', toggleFullscreen)
    isFullscreen.value = false
  } else {
    globalThis.addEventListener('keyup', toggleFullscreen)
    isFullscreen.value = true
  }
}

const step = ref<ResultCard>()

async function seeSteps () {
  if ((card as ContentCard).name === 'diff') {
    step.value = {
      title: 'Derivative Steps',
      output: await evalCard('diffsteps', input, (card as ContentCard).variable, {})
    }
  } else if ((card as ContentCard).name === 'integral_alternate') {
    step.value = {
      title: 'Integral Steps',
      output: await evalCard('intsteps', input, (card as ContentCard).variable, {})
    }
  }
}
</script>

<template>
  <beta-ambiguity
    v-if="'ambiguity' in card"
    :ambiguity="card.ambiguity"
    :description="card.description"
  />
  <n-card
    v-else
    :title="card.title"
    :class="['result_card', {
      result_card_error: 'error' in card || cardResult && 'error' in cardResult,
      fullscreen: isFullscreen
    }]"
    @keyup.esc="toggleFullscreen"
  >
    <template #header-extra>
      <beta-source-button
        v-if="'source' in card"
        :source="card.source"
      />
      <beta-wiki-button
        v-if="'wiki' in card"
        :wiki="card.wiki"
      />
    </template>
    <div v-if="'input' in card">
      <n-code
        v-if="typeof card.input === 'string'"
        :code="card.input"
        language="python"
        inline
        style="word-break: break-all"
      />
      <template v-else>
        plot([
        <template v-for="f, index in card.input">
          {{ index ? ", " : "" }}
          <span
            :style="{ color: colors(index), cursor: 'pointer' }"
            title="Click to toggle visibility"
            @click="toggleVisibility(index, $event)"
            @mouseenter="highlight(index, true)"
            @mouseleave="highlight(index, false)"
          >
            {{ f }}
            <component
              :is="visibility[index] === false ? EyeSlash : Eye"
              style="color: #000; width: 16px; margin-left: 5px"
            />
          </span>
        </template>])
      </template>
    </div>

    <div class="cell_output">
      <vue-mathjax
        v-if="'pre_output' in card && card.pre_output"
        :formula="'$' + card.pre_output + ' = $'"
      />
      <template v-if="'output' in card">
        <beta-container :content="card.output" />
        <div v-if="'variables' in card">
          Evaluate with respect to …
          <n-space>
            <n-button
              v-for="variable in card.variables"
              :disabled="variable === card.variable"
              secondary
              type="primary"
              @click="chooseVariable(variable)"
            >
              {{ variable }}
            </n-button>
          </n-space>
        </div>
      </template>
      <template v-else-if="'name' in card">
        <div
          v-if="'error' in cardResult"
          class="cell_output_plain"
        >
          {{ cardResult.error }}
        </div>
        <beta-container
          v-else-if="'type' in cardResult"
          :content="cardResult"
          :callback="{ getPlot, toggleFullscreen }"
        />
        <div
          v-else
          style="text-align: center"
        >
          <n-spin
            size="large"
          />
        </div>
      </template>
      <div
        v-else-if="'error' in card"
        class="cell_output_plain"
      >
        {{ card.error }}
      </div>
    </div>
    <beta-option
      v-if="numericCallbacks.length"
      name="More Digits"
      :callback="moreDigits"
    />
    <beta-option
      v-if="'name' in card && (card.name === 'diff' || card.name === 'integral_alternate') && !step"
      name="See Steps"
      :callback="seeSteps"
    />
  </n-card>
  <beta-card
    v-if="step"
    :card="step"
    :input="(card as ContentCard).input"
  />
</template>

<style>
.result_card {
  box-shadow: 0px 0px 5px 2px rgba(0, 0, 0, 0.2);
  width: calc(100vw - 24px);
  max-width: 1280px;
  margin: auto;
}

.result_card.result_card_error {
  border: 2px solid #f33;
  opacity: 0.7;
}

.result_card.result_card_error .cell_output_plain {
  white-space: pre;
  text-align: left;
}

/* Highlight position of a syntax error */
.result_card_error .cell_output_plain span:first-child {
  border-right: 1px solid #f33;
}

.result_card .card_options {
  font-size: 1em;
  font-family: "Open Sans", sans-serif;
  text-align: left;
  padding-top: 5px;
}

.result_card .card_options h2 {
  font-size: 1em;
  margin: 0.5em 0;
  padding: 0;
}

.result_card .card_options label {
  margin-left: 0.25em;
}
</style>
