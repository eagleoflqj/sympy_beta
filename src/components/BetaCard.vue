<script setup>
import { ref, reactive, onMounted, toRaw } from 'vue'
import { NButton, NSpace, NSpin, NCard } from 'naive-ui'
import { Eye, EyeSlash } from '@vicons/fa'
import { evcd } from '@/js/workerAPI.js'
import { Plot2D } from '@/js/plot.js'
import BetaAmbiguity from '@/components/BetaAmbiguity.vue'
import BetaContainer from '@/components/BetaContainer.vue'
import BetaOption from '@/components/BetaOption.vue'

const props = defineProps({
  cell: {
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

const { cell, input } = toRaw(props)

const cardResult = reactive({})

let digits = 15
const numericCallbacks = reactive([])

onMounted(async () => {
  if (typeof cell.card === 'undefined') {
    if (cell.ambiguity) {
      return
    }
    const numerics = []
    if (cell.output.numeric) {
      numerics.push(cell.output)
    } else if (cell.output.list) {
      cell.output.list.forEach(item => item.numeric && numerics.push(item))
    }
    numerics.forEach(item => numericCallbacks.push(async () =>
      Object.assign(item, await evcd('approximator', item.expression, 'x', { digits }))))
  } else {
    const hasDigits = cell.parameters.indexOf('digits') >= 0
    const evaluate = async () => {
      const parameters = hasDigits ? { digits } : {}
      Object.assign(cardResult, await evcd(cell.card, input, cell.variable, parameters))
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
    const { graphs } = await evcd(cell.card, input, cell.variable, parameters)
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
  if (cell.card === 'diff') {
    step.value = {
      title: 'Derivative Steps',
      output: await evcd('diffsteps', input, cell.variable, {})
    }
  } else if (cell.card === 'integral_alternate') {
    step.value = {
      title: 'Integral Steps',
      output: await evcd('intsteps', input, cell.variable, {})
    }
  }
}
</script>

<template>
  <beta-ambiguity
    v-if="cell.ambiguity"
    :ambiguity="cell.ambiguity"
    :description="cell.description"
  />
  <n-card
    v-else
    :title="cell.title"
    :class="['result_card', {
      result_card_error: cell.error || cell.exception_info || cardResult && cardResult.error,
      fullscreen: isFullscreen
    }]"
    @keyup.esc="toggleFullscreen"
  >
    <div v-if="cell.input">
      <template v-if="typeof cell.input === 'string'">
        {{ cell.input }}
      </template>
      <template v-else>
        plot([
        <template v-for="f, index in cell.input">
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
      <div
        v-if="cell.pre_output"
        class="cell_pre_output"
      >
        <vue-mathjax :formula="'$' + cell.pre_output + ' = $'" />
      </div>
      <template v-if="cell.output">
        <beta-container :card="cell.output" />
        <div v-if="cell.num_variables > 1">
          Evaluate with respect to …
          <n-space>
            <n-button
              v-for="variable in cell.variables"
              :disabled="variable === cell.variable"
              type="primary"
              @click="chooseVariable(variable)"
            >
              {{ variable }}
            </n-button>
          </n-space>
        </div>
      </template>
      <template v-else-if="cell.card">
        <div v-if="cell.cell_output">
          {{ cell.cell_output }}
        </div>
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
        <n-spin
          v-else
          size="large"
        />
      </template>
      <template v-else-if="cell.exception_info">
        <!-- {% if cell.exception_info.input_start %}
      <div class="cell_output_plain">
        <span>{{ cell.exception_info.input_start }}</span>
        <span>{{ cell.exception_info.input_end }}</span>
      </div>
      {% endif %}
      <div
        class="cell_output_plain"
        >{% if cell.exception_info.offset %}{{ cell.exception_info.offset }}: {% endif %}{{ cell.exception_info.msg }}</div>-->
      </template>
      <div
        v-else-if="cell.error"
        class="cell_output_plain"
      >
        {{ cell.error }}
      </div>
    </div>
    <beta-option
      v-if="numericCallbacks.length"
      name="More Digits"
      :callback="moreDigits"
    />
    <beta-option
      v-if="(cell.card === 'diff' || cell.card === 'integral_alternate') && step === null"
      name="See Steps"
      :callback="seeSteps"
    />
    <template
      v-if="cardResult.type === 'FactorDiagram'"
      #footer
    >
      <a
        href="https://mathlesstraveled.com/2012/10/05/factorization-diagrams/"
        target="_blank"
      >About this diagram</a>
    </template>
  </n-card>
  <beta-card
    v-if="step !== null"
    :cell="step"
    :input="cell.input"
  />
</template>
