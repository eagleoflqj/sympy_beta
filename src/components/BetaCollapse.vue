<script setup>
import { NCard, NCollapse, NCollapseItem, NA } from 'naive-ui'

defineProps({
  category: {
    type: Object,
    default: () => {}
  }
})
</script>

<template>
  <n-card>
    <n-collapse class="example-group">
      <n-collapse-item :title="category.name">
        <div style="padding: 0.5em">
          <div v-for="sub_category in category.sub_categorys">
            <h4 v-if="sub_category.name">
              {{ sub_category.name }}
            </h4>
            <ul>
              <li v-for="example in sub_category.examples">
                <span
                  v-if="example.name && example.html"
                  v-html="example.name"
                />
                <span v-else-if="example.name">{{ example.name }}</span>
                <router-link
                  :to="{ name: 'Python', params: { expr: example.expression } }"
                >
                  <n-a>{{ example.expression }}</n-a>
                </router-link>
              </li>
            </ul>
          </div>
        </div>
      </n-collapse-item>
    </n-collapse>
  </n-card>
</template>

<style scoped>
.example-group i {
  cursor: pointer;
  float: left;
  margin: 0.3em 0.2em 0.3em 0.4em;
  font-size: 1.25em;
}

.example-group h4 {
  font-size: 15px;
}

.example-group a {
  text-decoration: none;
  font-family: "Droid Sans Mono", monospace;
  font-size: 15px;
}

.example-group li > span {
  display: block;
  padding: 0.125em 0;
  font-style: italic;
  font-size: 15px;
}
</style>
