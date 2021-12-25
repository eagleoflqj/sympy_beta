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
  <n-card class="did_you_mean">
    Did you mean:
    <router-link :to="{ name: 'Result', params: { expr: ambiguity } }">
      {{ ambiguity }}
    </router-link>?
    <br>
    <template v-for="item in description">
      <template v-if="item.type === 'Expression'">
        <router-link :to="{ name: 'Result', params: { expr: item.value } }">
          {{ item.value }}
        </router-link>
      </template>
      <template v-else-if="item.type === 'Text'">
        {{ item.value }}
      </template>
    </template>
  </n-card>
</template>

<style>
.did_you_mean {
  text-align: center;
  box-shadow: 0px 0px 5px 2px rgba(255, 127, 14, 0.5);
}

@media screen and (max-device-width: 767px) {
  .did_you_mean {
    box-shadow: none;
    border: 1px solid #f33;
  }
}
</style>
