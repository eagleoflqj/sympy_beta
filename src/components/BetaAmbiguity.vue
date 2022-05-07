<script setup>
import { NCard } from 'naive-ui'

defineProps({
  ambiguity: {
    type: String,
    default: () => ''
  },
  description: {
    type: Array,
    default: () => []
  }
})
</script>

<template>
  <n-card
    class="result_card"
    style="text-align: center;
  box-shadow: 0px 0px 5px 2px rgba(255, 127, 14, 0.5)"
  >
    Did you mean:
    <router-link :to="{ name: 'Python', params: { expr: ambiguity } }">
      {{ ambiguity }}
    </router-link>?
    <br>
    <template v-for="item in description">
      <router-link
        v-if="item.type === 'Expression'"
        :to="{ name: 'Python', params: { expr: item.value } }"
      >
        {{ item.value }}
      </router-link>
      <template v-else-if="item.type === 'Text'">
        {{ item.value }}
      </template>
    </template>
  </n-card>
</template>
