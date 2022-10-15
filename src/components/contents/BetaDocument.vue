<script setup lang="ts">
defineProps<{
  content: DocumentContent
}>()
</script>

<template>
  <div v-html="content.html" />
</template>

<style>
/* Documentation */

.document {
  text-align: left;
  font-size: 0.9em;
  font-family: "Open Sans", sans-serif;
}

.document p {
  margin: 0.25em 0;
  padding: 0;
}

.document h1 {
  font-family: inherit;
  color: #000;
  font-size: 1.2em;
  line-height: 1.25em;
  margin: 0.25em 0 0.5em 0;
}

.document pre {
  background-color: #eeffcc;
  color: #333333;
  padding: 5px;
  border: 1px solid #ac9;
  border-left: none;
  border-right: none;
}
</style>
