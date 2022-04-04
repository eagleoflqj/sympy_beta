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

onMounted(() => {
  img.value.src = `data:image/svg+xml;base64,${props.card.svg}`
})
</script>

<template>
  <div style="text-align: right">
    <beta-download-image-button
      :img="img"
      :name="card.name"
    />
  </div>
  <img
    ref="img"
    style="height: 50px"
  >
</template>
