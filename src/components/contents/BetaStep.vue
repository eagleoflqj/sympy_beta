<script setup lang="ts">
defineProps<{
  content: Step
}>()
</script>

<template>
  <ol v-if="content.level">
    <beta-step
      v-for="item in content.level"
      :content="item"
    />
  </ol>
  <li v-else-if="content.step">
    <beta-step
      v-for="item in content.step"
      :content="item"
    />
  </li>
  <p v-else-if="content.p">
    <beta-step
      v-for="item in content.p"
      :content="item"
    />
  </p>
  <div
    v-else-if="content.collapsible"
    class="collapsible"
  >
    <beta-step
      v-for="item in content.collapsible"
      :content="item"
    />
  </div>
  <template v-else-if="content.text">
    {{ content.text }}
  </template>
  <vue-mathjax
    v-else-if="content.inline"
    :formula="'$' + content.inline + '$'"
  />
  <vue-mathjax
    v-else-if="content.block"
    :formula="'$$' + content.block + '$$'"
  />
  <h2 v-else-if="content.header">
    {{ content.header }}
  </h2>
</template>
