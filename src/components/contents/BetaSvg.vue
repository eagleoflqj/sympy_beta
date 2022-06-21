<script setup>
import { ref, onMounted } from 'vue'
import BetaDownloadImageButton from '@/components/BetaDownloadImageButton.vue'

const props = defineProps({
  card: {
    type: Object,
    default: () => {}
  }
})

const img = ref(null)
const name = `${props.card.category}.svg`

onMounted(() => {
  img.value.src = `data:image/svg+xml;base64,${props.card.svg}`
})
</script>

<template>
  <div style="text-align: right">
    <beta-download-image-button
      :img="img"
      :name="name"
    />
  </div>
  <img
    ref="img"
    :class="card.category"
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
