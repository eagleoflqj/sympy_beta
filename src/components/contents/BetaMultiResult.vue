<script setup lang="ts">
import { NCode } from 'naive-ui'
import BetaContainer from '../BetaContainer.vue'

defineProps<{
  content: MultiResultContent
}>()
</script>

<template>
  <ul>
    <li v-for="result in content.results">
      <n-code
        :code="result.input"
        language="python"
        inline
      />
      <beta-container :content="result.output" />
    </li>
  </ul>
</template>
