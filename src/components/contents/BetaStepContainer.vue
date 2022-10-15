<script setup lang="ts">
import BetaStep from '../contents/BetaStep.vue'

defineProps<{
  content: StepContainerContent
}>()
</script>

<template>
  <div class="steps">
    <beta-step :content="content.content" />
    <hr>
    <p>The answer is:</p>
    <beta-step :content="content.answer" />
  </div>
</template>

<style>
/* Derivative/integral steps */

.steps {
  text-align: left;
  font-size: 0.9em;
  font-family: "Open Sans", sans-serif;
  max-width: 1600px;
  overflow: auto;
  margin: auto;
}

.steps li {
  min-width: 300px;
}

/* colors from http://gamedev.stackexchange.com/questions/46463 */
.steps ol {
  list-style-type: decimal;
  border-left: 1px solid #ff8080;
  padding: 0 30px;
}
.steps ol h2 {
  border-bottom: 1px solid #ff8080;
}

.steps ol ol {
  list-style-type: upper-alpha;
  border-left: 1px solid #92d169;
}

.steps ol ol h2 {
  border-bottom: 1px solid #92d169;
}

.steps ol ol ol {
  list-style-type: upper-roman;
  border-left: 1px solid #78bef0;
}

.steps ol ol ol h2 {
  border-bottom: 1px solid #78bef0;
}

.steps ol ol ol ol {
  list-style-type: lower-alpha;
  border-left: 1px solid #cc66c9;
}

.steps ol ol ol ol h2 {
  border-bottom: 1px solid #cc66c9;
}

.steps ol ol ol ol ol {
  list-style-type: lower-roman;
  border-left: 1px solid #f2a279;
}

.steps ol ol ol ol ol h2 {
  border-bottom: 1px solid #f2a279;
}
</style>
