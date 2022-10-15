<script setup lang="ts">
import { NTable, NText } from 'naive-ui'
import BetaCopyMarkdownButton from '../BetaCopyMarkdownButton.vue'

defineProps<{
  content: TruthTableContent
}>()
</script>

<template>
  <div
    style="text-align: right"
  >
    <beta-copy-markdown-button
      :thead="content.titles"
      :tbody="content.rows"
    />
  </div>
  <n-table
    :single-line="false"
    striped
    style="width: 0; margin: auto; word-break: keep-all"
  >
    <thead>
      <tr>
        <th v-for="title in content.titles">
          {{ title }}
        </th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="row in content.rows">
        <td v-for="cell in row">
          <n-text :type="cell === 'True' ? 'success' : 'error'">
            {{ cell }}
          </n-text>
        </td>
      </tr>
    </tbody>
  </n-table>
</template>
