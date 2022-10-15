<script setup lang="ts">
import { ref, watch } from 'vue'
import { NSwitch, NIcon, NCheckbox, NSpace, darkTheme, useOsTheme } from 'naive-ui'
import { Moon, Sun } from '@vicons/tabler'
import { isMobile } from '../util'
import BetaShowMenu from './BetaShowMenu.vue'

const props = defineProps<{
  setTheme: (theme: GlobalTheme) => void
}>()

const osThemeRef = useOsTheme()
const followSystem = ref(true)
const switchValueRef = ref()

function updateTheme (theme: 'dark' | 'light' | null, isAuto?: boolean) {
  if (!isAuto) {
    props.setTheme(theme === 'dark' ? darkTheme : null)
    followSystem.value = false
  }
  switchValueRef.value = theme
}

function followOSTheme () {
  props.setTheme(osThemeRef.value === 'dark' ? darkTheme : null)
  updateTheme(osThemeRef.value, true)
}

followOSTheme()

watch(followSystem, newValue => newValue && followOSTheme())

watch(osThemeRef, () => followSystem.value && followOSTheme())
</script>

<template>
  <component :is="isMobile ? BetaShowMenu : 'div'">
    <n-space :vertical="isMobile">
      <n-switch
        unchecked-value="light"
        checked-value="dark"
        :value="switchValueRef"
        @update:value="updateTheme"
      >
        <template #unchecked-icon>
          <n-icon :component="Sun" />
        </template>
        <template #unchecked>
          Light
        </template>
        <template #checked>
          Dark
        </template>
        <template #checked-icon>
          <n-icon :component="Moon" />
        </template>
      </n-switch>
      <n-checkbox v-model:checked="followSystem">
        Follow System
      </n-checkbox>
    </n-space>
  </component>
</template>
