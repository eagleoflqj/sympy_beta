<script setup>
import { ref, reactive, onMounted, toRaw } from 'vue'
import { NButton, NSpace, NSpin, NCard, NCode } from 'naive-ui'
import { Eye, EyeSlash } from '@vicons/fa'
import { evalCard } from '@/js/workerAPI.js'
import { Plot2D } from '@/js/plot.js'
import BetaAmbiguity from '@/components/BetaAmbiguity.vue'
import BetaContainer from '@/components/BetaContainer.vue'
import BetaOption from '@/components/BetaOption.vue'
import BetaSourceButton from '@/components/BetaSourceButton.vue'

const props = defineProps({
  card: {
    type: Object,
    default: () => {}
  },
  input: {
    type: String,
    default: () => ''
  },
  chooseVariable: {
    type: Function,
    default: () => () => {}
  }
})

const { card, input } = toRaw(props)

const cardResult = reactive({})

let digits = 15
const numericCallbacks = reactive([])

onMounted(async () => {
  if (typeof card.name === 'undefined') {
    if (card.ambiguity || card.error) {
      return
    }
    const numerics = []
    if (card.output.numeric) {
      numerics.push(card.output)
    } else if (card.output.list) {
      card.output.list.forEach(item => item.numeric && numerics.push(item))
    }
    numerics.forEach(item => numericCallbacks.push(async () =>
      Object.assign(item, await evalCard('approximator', item.expression, 'x', { digits }))))
  } else {
    const hasDigits = (card.parameters || []).indexOf('digits') >= 0
    const evaluate = async () => {
      const parameters = hasDigits ? { digits } : {}
      Object.assign(cardResult, await evalCard(card.name, input, card.variable, parameters))
    }
    evaluate()
    if (hasDigits) {
      numericCallbacks.push(evaluate)
    }
  }
})

function moreDigits () {
  digits += 10
  numericCallbacks.forEach(callback => callback())
}

let plot = null
const colors = d3.scale.category10()

function getPlot (container) {
  plot = new Plot2D(container, cardResult.graphs, async (parameters) => {
    const { graphs } = await evalCard(card.name, input, card.variable, parameters)
    return graphs
  })
  return plot
}

const visibility = ref({})

function toggleVisibility (index, event) {
  if (plot !== null) {
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

function highlight (index, highlight) {
  if (plot !== null) {
    plot.highlight(index, highlight)
  }
}

const isFullscreen = ref(false)

function toggleFullscreen (event) {
  if (event.type === 'keyup' && event.keyCode !== 27) {
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

const step = ref(null)

async function seeSteps () {
  if (card.name === 'diff') {
    step.value = {
      title: 'Derivative Steps',
      output: await evalCard('diffsteps', input, card.variable, {})
    }
  } else if (card.name === 'integral_alternate') {
    step.value = {
      title: 'Integral Steps',
      output: await evalCard('intsteps', input, card.variable, {})
    }
  }
}
</script>

<template>
  <beta-ambiguity
    v-if="card.ambiguity"
    :ambiguity="card.ambiguity"
    :description="card.description"
  />
  <n-card
    v-else
    :title="card.title"
    :class="['result_card', {
      result_card_error: card.error || cardResult && cardResult.error,
      fullscreen: isFullscreen
    }]"
    @keyup.esc="toggleFullscreen"
  >
    <template
      v-if="card.source"
      #header-extra
    >
      <beta-source-button :source="card.source" />
    </template>
    <div v-if="card.input">
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
        v-if="card.pre_output"
        :formula="'$' + card.pre_output + ' = $'"
      />
      <template v-if="card.output">
        <beta-container :card="card.output" />
        <div v-if="card.num_variables > 1">
          Evaluate with respect to …
          <n-space>
            <n-button
              v-for="variable in card.variables"
              :disabled="variable === card.variable"
              type="primary"
              @click="chooseVariable(variable)"
            >
              {{ variable }}
            </n-button>
          </n-space>
        </div>
      </template>
      <template v-else-if="card.name">
        <div
          v-if="cardResult.error"
          class="cell_output_plain"
        >
          {{ cardResult.error }}
        </div>
        <beta-container
          v-else-if="cardResult.type"
          :card="cardResult"
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
        v-else-if="card.error"
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
      v-if="(card.name === 'diff' || card.name === 'integral_alternate') && step === null"
      name="See Steps"
      :callback="seeSteps"
    />
  </n-card>
  <beta-card
    v-if="step !== null"
    :card="step"
    :input="card.input"
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
