<script setup>
import { NTable, NText } from 'naive-ui'

defineProps({
  card: {
    type: Object,
    default: () => {}
  }
})
</script>

<template>
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
