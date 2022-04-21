<script setup>
import { h, computed } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { NMenu } from 'naive-ui'

import BetaSwitchTheme from '@/components/BetaSwitchTheme.vue'

defineProps({
  setTheme: {
    type: Function,
    required: true
  }
})

const route = useRoute()

const menuOptions = [
  {
    label: () => h(RouterLink, {
      to: {
        name: 'Main'
      }
    }, () => 'Main'),
    key: 'Main'
  },
  {
    label: () => h(RouterLink, {
      to: {
        name: 'Terminal'
      }
    }, () => 'Pyodide Terminal'),
    key: 'Terminal'
  }
]

const menuValue = computed(() => {
  return route.name
})
</script>

<template>
  <n-menu
    mode="horizontal"
    :value="menuValue"
    :options="menuOptions"
  />
  <beta-switch-theme :set-theme="setTheme" />
</template>
