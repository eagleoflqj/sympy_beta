<script setup>
import { NTable, NScrollbar } from 'naive-ui'
import BetaContainer from '@/components/BetaContainer.vue'
import { onMounted } from 'vue'

const props = defineProps({
  card: {
    type: Object,
    default: () => {}
  }
})

const maxNRow = 10
onMounted(() => {
  const { card } = props
  const nColumn = Math.ceil(card.rows.length / maxNRow)
  card.titles.splice(0, card.titles.length, ...[].concat(...new Array(nColumn).fill(card.titles)))
  const remainingRows = card.rows.splice(maxNRow)
  for (const i in remainingRows) {
    const j = i % maxNRow
    card.rows[j].splice(card.rows[j].length, 0, ...remainingRows[i])
  }
})
</script>

<template>
  <n-scrollbar x-scrollable>
    <n-table style="width: 0; margin: auto">
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
            <beta-container
              v-if="typeof cell === 'object'"
              :card="cell"
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
