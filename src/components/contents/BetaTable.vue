<script setup>
import { NTable } from 'naive-ui'
import BetaContainer from '@/components/BetaContainer.vue'

defineProps({
  card: {
    type: Object,
    default: () => {}
  }
})
</script>

<template>
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
</template>
