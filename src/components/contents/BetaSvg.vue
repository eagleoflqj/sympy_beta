<script setup lang="ts">
import { ref, onMounted } from 'vue'
import BetaDownloadImageButton from '../BetaDownloadImageButton.vue'

const props = defineProps<{
  content: SvgContent
}>()

const img = ref<HTMLImageElement>()
const name = `${props.content.category}.svg`

onMounted(() => {
  img.value!.src = `data:image/svg+xml;base64,${props.content.svg}`
})
</script>

<template>
  <div style="text-align: right">
    <beta-download-image-button
      :img="img!"
      :name="name"
    />
  </div>
  <img
    ref="img"
    :class="content.category"
  >
</template>

<style scoped>
.pie_chart {
  height: 50px;
}

.plot_3d, .plot_complex, .plot_contour {
  width: 100%;
  max-width: 500px;
}
</style>
