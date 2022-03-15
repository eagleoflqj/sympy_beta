<script setup>
import { NTable, NText } from 'naive-ui'
import BetaCopyMarkdownButton from '@/components/BetaCopyMarkdownButton.vue'

defineProps({
  card: {
    type: Object,
    required: true
  }
})
</script>

<template>
  <div
    style="
  text-align: right"
  >
    <beta-copy-markdown-button
      :thead="card.titles"
      :tbody="card.rows"
    />
  </div>
  <n-table
    :single-line="false"
    striped
    style="width: 0; margin: auto"
  >
    <thead>
      <tr>
        <th v-for="title in card.titles">
          {{ title }}
        </th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="row in card.rows">
        <td v-for="cell in row">
          <n-text :type="cell === 'True' ? 'success' : 'error'">
            {{ cell }}
          </n-text>
        </td>
      </tr>
    </tbody>
  </n-table>
</template>
