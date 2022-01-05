<script setup>
import { ref, reactive, watchEffect } from 'vue'
import { useRoute } from 'vue-router'
import { NSpace, NSpin } from 'naive-ui'
import { ev } from '@/js/workerAPI.js'
import BetaSearch from '@/components/BetaSearch.vue'
import BetaCard from '@/components/BetaCard.vue'

const route = reactive(useRoute())
const expr = ref('')
const variableRef = ref(null)
const result = reactive([])

watchEffect(async () => {
  if (typeof route.params.expr === 'undefined') {
    return
  }
  expr.value = route.params.expr
  result.splice(0)
  result.push(...await ev(expr.value, variableRef.value))

  // TODO: finish integration with Sphinx
  // setupDocumentation();
})

function chooseVariable (variable) {
  variableRef.value = variable
}
</script>

<template>
  <n-space
    size="large"
    vertical
  >
    <beta-search :expr="expr" />
    <div
      v-if="result.length === 0"
      style="text-align: center"
    >
      <n-spin />
    </div>
    <beta-card
      v-for="cell, index in result"
      :key="'card' + expr + index"
      :cell="cell"
      :input="expr"
      :choose-variable="chooseVariable"
    />
    <div class="foot">
      See what
      <a
        class="wolfram"
        :href="'https://www.wolframalpha.com/input/?i=' + encodeURIComponent(expr)"
        target="_blank"
      >Wolfram|Alpha</a> says.
    </div>
  </n-space>
</template>
