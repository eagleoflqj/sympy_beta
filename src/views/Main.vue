<script setup>
import { useRouter } from 'vue-router'
import { NButton } from 'naive-ui'
import BetaSearch from '@/components/BetaSearch.vue'
import BetaCollapse from '@/components/BetaCollapse.vue'
import categorys from '@/js/categorys.js'

const router = useRouter()

function randomExample () {
  const examples = []
  for (const category of categorys) {
    for (const subCategory of category.sub_categorys) {
      for (const example of subCategory.examples) {
        examples.push(example.expression)
      }
    }
  }
  const example = examples[Math.floor(Math.random() * examples.length)]
  router.push({ name: 'Result', params: { expr: example } })
}
</script>

<template>
  <beta-search />
  <div class="col example">
    <h2>Examples</h2>
    <n-button
      type="primary"
      @click="randomExample"
    >
      Random Example
    </n-button>
    <beta-collapse
      v-for="category, index in categorys"
      :key="'collapse' + index"
      :category="category"
    />
    <p>
      … and more: see
      the
      <a href="https://docs.sympy.org">documentation</a> to learn
      about the full range of SymPy's capabilities.
    </p>
  </div>
</template>
