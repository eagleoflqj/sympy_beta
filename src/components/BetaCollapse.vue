<script setup>
import { NCollapse, NCollapseItem } from 'naive-ui'

defineProps({
  category: {
    type: Object,
    default: () => {}
  }
})
</script>

<template>
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
                :to="{ name: 'Result', params: { expr: example.expression } }"
              >
                {{ example.expression }}
              </router-link>
            </li>
          </ul>
        </div>
      </div>
    </n-collapse-item>
  </n-collapse>
</template>

<style>
.n-collapse-item__header {
  --title-font-size: 16px;
}

.n-collapse
  .n-collapse-item
  .n-collapse-item__content-wrapper
  .n-collapse-item__content-inner {
  padding-top: 0;
}

.example-group {
  background: #fff;
  margin: 0.5em 0;
  box-shadow: 0px 0px 1px 1px rgba(0, 0, 0, 0.2);
}

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
  color: #3b5526;
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
