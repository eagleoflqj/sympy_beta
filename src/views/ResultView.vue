<script setup>
import { ref, reactive, watchEffect } from 'vue'
import { useRoute } from 'vue-router'
import { NSpace, NSpin, NA } from 'naive-ui'
import { evalInput, evalLatexInput } from '@/js/workerAPI.js'
import BetaSearch from '@/components/BetaSearch.vue'
import BetaCard from '@/components/BetaCard.vue'
import { homepage } from '@/../package.json'

const route = useRoute()
const expr = ref('')
const variableRef = ref(null)
const cards = reactive([])

watchEffect(async () => {
  const routeExpr = route.params.expr
  if (typeof routeExpr === 'undefined') {
    return
  }
  cards.splice(0)
  if (route.name === 'LaTeX') {
    const { result, error } = await evalLatexInput(routeExpr)
    if (error) {
      cards.push({ error })
      return
    }
    expr.value = result
  } else {
    expr.value = routeExpr
  }
  const { result, error } = await evalInput(expr.value, variableRef.value)
  if (result) {
    cards.push(...result)
  } else {
    cards.push({ error })
  }
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
    <beta-search />
    <div
      v-if="cards.length === 0"
      style="text-align: center"
    >
      <n-spin />
    </div>
    <beta-card
      v-for="card in cards"
      :card="card"
      :input="expr"
      :choose-variable="chooseVariable"
    />
    <div class="foot">
      See what
      <n-a
        class="wolfram"
        :href="`https://www.wolframalpha.com/input/?i=${encodeURIComponent(expr)}`"
        target="_blank"
      >
        Wolfram|Alpha
      </n-a> says.
      <p>
        This page needs improvement? <n-a
          :href="`${homepage}/issues/new?title=Improvement suggestion&body=%23%23 Input%0A\`${encodeURIComponent(expr)}\`%0A%23%23 How can it be better?%0A`"
          target="_blank"
        >
          Submit an issue
        </n-a>!
      </p>
    </div>
  </n-space>
</template>
