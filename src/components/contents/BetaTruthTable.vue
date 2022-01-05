<script setup>
defineProps({
  card: {
    type: Object,
    default: () => {}
  }
})
</script>

<template>
  <table>
    <thead>
      <tr>
        <th v-for="title in card.titles">
          {{ title }}
        </th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="row in card.rows">
        <td
          v-for="cell in row.slice(0, -1)"
          :class="cell.toLowerCase()"
        >
          {{ cell }}
        </td>
        <td>{{ row.at(-1) }}</td>
      </tr>
    </tbody>
  </table>
</template>

<style>
td.true {
  background-color: #3bb878;
}

td.false {
  background-color: #f7977a;
}
</style>
