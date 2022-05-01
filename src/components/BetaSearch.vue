<script setup>
import { ref, watchEffect } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { NInputGroup, NInput, NButton, NH1, NA, NPopover, NRadioGroup, NRadioButton, NIcon, NSpace, NCard, NScrollbar } from 'naive-ui'
import { Python } from '@vicons/fa'
import { Math } from '@vicons/tabler'

const input = ref()
const defaultInputType = 'Python'
const inputType = ref(defaultInputType)
const clickedPythonInput = ref(false)
const router = useRouter()

function submit () {
  clickedPythonInput.value = false
  if (input.value) {
    router.push({ name: 'Result', params: { expr: input.value, inputType: inputType.value } })
  }
}

/**
 * \, _{ and ^{ are LaTex patterns that are meaningless as Python input,
 * so automatically switch to LaTex input.
 * But if a user explicitly chooses Python input, don't switch.
*/
function checkSwitchToLaTex () {
  if (inputType.value === 'Python' && !clickedPythonInput.value && /\\|_\{|^\{/.test(input.value)) {
    inputType.value = 'LaTex'
  }
}

const route = useRoute()
watchEffect(() => {
  input.value = route.params.expr || ''
  inputType.value = route.params.inputType || defaultInputType
})
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
          @input="checkSwitchToLaTex"
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
        <n-radio-button value="LaTex">
          <n-icon :component="Math" />
          LaTex input
        </n-radio-button>
      </n-radio-group>
      <n-card v-if="inputType === 'LaTex'">
        <n-scrollbar x-scrollable>
          <vue-mathjax
            :formula="'$$' + input + '$$'"
          />
        </n-scrollbar>
      </n-card>
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
