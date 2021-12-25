<script setup>
import { h, computed } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { NMenu } from 'naive-ui'

const route = useRoute()

const menuOptions = [
  {
    label: () => h(RouterLink, {
      to: {
        name: 'Main'
      }
    }, () => 'Main'),
    key: 'Main'
  }
]

const menuValue = computed(() => {
  return route.name
})
</script>

<template>
  <div class="menu">
    <n-menu
      mode="horizontal"
      :value="menuValue"
      :options="menuOptions"
    />
  </div>
</template>
