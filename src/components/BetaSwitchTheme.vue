<script setup>
import { ref, watch } from 'vue'
import { NSwitch, NIcon, NCheckbox, NSpace, darkTheme, useOsTheme } from 'naive-ui'
import { useBreakpoint, useMemo } from 'vooks'
import { Moon, Sun } from '@vicons/tabler'
import BetaShowMenu from '@/components/BetaShowMenu.vue'

const props = defineProps({
  setTheme: {
    type: Function,
    required: true
  }
})

const isMobile = (() => {
  const breakpointRef = useBreakpoint()
  return useMemo(() => {
    return breakpointRef.value === 'xs'
  })
})() // copied from naive-ui (MIT)

const osThemeRef = useOsTheme()
const followSystem = ref(true)
const switchValueRef = ref()

function followOSTheme () {
  props.setTheme(osThemeRef.value === 'dark' ? darkTheme : null)
  updateTheme(osThemeRef.value, true)
}

followOSTheme()

watch(followSystem, newValue => newValue && followOSTheme())

watch(osThemeRef, () => followSystem.value && followOSTheme())

function updateTheme (theme, isAuto) {
  if (!isAuto) {
    props.setTheme(theme === 'dark' ? darkTheme : null)
    followSystem.value = false
  }
  switchValueRef.value = theme
}
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
