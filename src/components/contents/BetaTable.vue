<script setup lang="ts">
import { NTable, NScrollbar } from 'naive-ui'
import BetaTex from '../contents/BetaTex.vue'
import BetaCopyMarkdownButton from '../BetaCopyMarkdownButton.vue'
import { onMounted } from 'vue'

const props = defineProps<{
  content: TableContent
}>()

const maxNRow = 10
onMounted(() => {
  const { content } = props
  const nColumn = Math.ceil(content.rows.length / maxNRow)
  content.titles.splice(0, content.titles.length, ...[].concat(...Array(nColumn).fill(content.titles)))
  const remainingRows = content.rows.splice(maxNRow)
  for (const i in remainingRows) {
    const j = Number(i) % maxNRow
    content.rows[j].splice(content.rows[j].length, 0, ...remainingRows[i])
  }
})
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
  <n-scrollbar x-scrollable>
    <n-table style="width: 0; margin: auto; white-space: nowrap">
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
            <beta-tex
              v-if="typeof cell === 'object'"
              :content="cell"
              :show-copy-button="false"
            />
            <template v-else>
              {{ cell }}
            </template>
          </td>
        </tr>
      </tbody>
    </n-table>
  </n-scrollbar>
</template>
