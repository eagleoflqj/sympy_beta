<script setup>
import { ref, toRaw, onMounted } from 'vue'
import { NSpace, NButton, NCheckbox, NCheckboxGroup } from 'naive-ui'

const props = defineProps({
  callback: {
    type: Object,
    default: () => {}
  }
})

const { callback } = toRaw(props)

onMounted(setupPlots)

const container = ref(null)
let plot = null

function reset () {
  plot.reset()
  resizeContainer({
    reset: true
  })
}

function squareViewport () {
  const size = d3.max([plot.width(), plot.height()])
  resizeContainer({
    width: size,
    height: size
  })
}

function resizeContainer (options) {
  if (options.reset) {
    plot.reset()
    container.value.style.width = '60%'
    container.value.style.height = Math.round(plot.width() * 3 / 4) + 'px'
    return
  }
  container.value.style.width = options.width + 'px'
  container.value.style.height = options.height + 'px'
}

const plotOption = ref(['grid', 'axes', 'path'])

function changePlotOption (opt) {
  plot.setOption(plotOption.value)
  plot.update()
}

function exportSVG () {
  const a = document.createElement('a')
  a.href = plot.asDataURI()
  a.download = 'plot.svg'
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
}

function setupPlots () {
  plot = callback.getPlot(container.value)
  plot.show()

  const observer = new MutationObserver(function () {
    plot.resize()
  })
  observer.observe(container.value, {
    attributes: true
  })
}
</script>

<template>
  <div
    ref="container"
    class="plot"
  />
  <p class="help">
    Drag to pan, (shift-)double-click to zoom, drag corner to resize
  </p>
  <n-space vertical>
    <n-checkbox-group
      v-model:value="plotOption"
      @update:value="changePlotOption"
    >
      <n-checkbox
        v-for="opt in ['grid', 'axes', 'points', 'path']"
        :value="opt"
        :label="opt"
      />
    </n-checkbox-group>
    <n-space>
      <n-button
        type="primary"
        @click="reset"
      >
        Reset
      </n-button>
      <n-button
        type="primary"
        @click="squareViewport"
      >
        Square Viewport
      </n-button>
      <n-button
        type="primary"
        @click="callback.toggleFullscreen"
      >
        Fullscreen
      </n-button>
      <n-button
        type="primary"
        @click="exportSVG"
      >
        Export SVG
      </n-button>
    </n-space>
  </n-space>
</template>

<style>
.plot {
  width: 60%;
  aspect-ratio: 4/3;
  max-width: 80%;
  margin: 0 auto;
  overflow: hidden;
  resize: both;
}

.plot .graphs {
  display: none;
}

.plot svg {
  cursor: all-scroll;
}

.plot svg text {
  font-family: monospace;
  font-size: 0.875em;
}

.plot svg path:hover {
  stroke-width: 3;
}

.help {
  margin: 0;
  padding: 0;
  font-size: smaller;
  color: #555;
}
</style>
