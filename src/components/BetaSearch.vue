<script setup>
import { ref, watchEffect } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { NInputGroup, NInput, NButton, NH1, NA, NPopover, NRadioGroup, NRadioButton, NIcon, NSpace } from 'naive-ui'
import { Python } from '@vicons/fa'
import { Math } from '@vicons/tabler'
import BetaMathLive from '@/components/BetaMathLive.vue'

const input = ref()
const defaultInputType = 'Python'
const inputType = ref(defaultInputType)
const clickedPythonInput = ref(false)
const router = useRouter()

function submit () {
  clickedPythonInput.value = false
  if (input.value) {
    router.push({ name: inputType.value, params: { expr: input.value } })
  }
}

/**
 * \, _{ and ^{ are LaTeX patterns that are meaningless as Python input,
 * so automatically switch to LaTeX input.
 * But if a user explicitly chooses Python input, don't switch.
*/
function checkSwitchToLaTeX () {
  if (inputType.value === 'Python' && !clickedPythonInput.value && /\\|_\{|^\{/.test(input.value)) {
    inputType.value = 'LaTeX'
  }
}

const route = useRoute()
watchEffect(() => {
  input.value = route.params.expr || ''
  inputType.value = route.name === 'LaTeX' ? 'LaTeX' : defaultInputType
})

function mathliveInputCallback (value) {
  input.value = value
}
</script>

<template>
  <div
    class="input"
  >
    <n-h1>
      <router-link :to="'/'">
        <img
          src="/favicon.svg"
          alt=""
        >
        <n-a>SymPy Beta</n-a>
      </router-link>
    </n-h1>
    <n-space vertical>
      <n-input-group>
        <n-input
          v-model:value="input"
          type="text"
          placeholder
          clearable
          style="font-family: 'Droid Sans Mono', monospace"
          @keyup.enter="submit"
          @input="checkSwitchToLaTeX"
        />
        <n-popover>
          <template #trigger>
            <n-button
              type="primary"
              @click="submit"
            >
              =
            </n-button>
          </template>
          compute input
        </n-popover>
      </n-input-group>
      <n-radio-group v-model:value="inputType">
        <n-radio-button
          value="Python"
          @click="clickedPythonInput = true"
        >
          <n-icon :component="Python" />
          Python input
        </n-radio-button>
        <n-radio-button value="LaTeX">
          <n-icon :component="Math" />
          LaTeX input
        </n-radio-button>
      </n-radio-group>
      <beta-math-live
        v-show="inputType === 'LaTeX'"
        :input="input"
        :input-callback="mathliveInputCallback"
        :enter-callback="submit"
      />
    </n-space>
  </div>
</template>

<style scoped>
h1 {
  margin-bottom: 0;
  text-align: center;
}

h1 a {
  text-decoration: none;
}

h1 a img {
  vertical-align: middle;
}

img {
  height: 75px
}

.input {
  width: calc(100vw - 24px);
  max-width: 584px;
  margin: auto;
  padding-bottom: 20px;
  display: flex;
  flex-direction: column;
}
</style>
