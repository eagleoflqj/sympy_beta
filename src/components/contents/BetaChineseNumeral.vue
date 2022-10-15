<script setup lang="ts">
import { ref, computed } from 'vue'
import { NSpace, NSwitch, NIcon } from 'naive-ui'
import { AbcFilled, AttachMoneyFilled } from '@vicons/material'
import BetaCopyTextButton from '../BetaCopyTextButton.vue'

const props = defineProps<{
  content: ChineseNumeralContent
}>()

const financial = ref(false)
const text = computed(() => financial.value ? props.content.financial : props.content.normal)
</script>

<template>
  <n-space vertical>
    <div style="display: flex; justify-content: space-between">
      <n-switch v-model:value="financial">
        <template #checked>
          financial
        </template>
        <template #checked-icon>
          <n-icon :component="AttachMoneyFilled" />
        </template>
        <template #unchecked-icon>
          <n-icon :component="AbcFilled" />
        </template>
        <template #unchecked>
          normal
        </template>
      </n-switch>
      <beta-copy-text-button :text="text" />
    </div>
    {{ text }}
  </n-space>
</template>
