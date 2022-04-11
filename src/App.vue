<script setup>
import { ref, watchEffect } from 'vue'
import { useRoute } from 'vue-router'
import { NNotificationProvider, NLayout, NLayoutHeader, NLayoutContent, NLayoutFooter, NBackTop, NMessageProvider } from 'naive-ui'
import BetaHeader from '@/components/BetaHeader.vue'
import BetaFooter from '@/components/BetaFooter.vue'
import RuntimeLoader from '@/components/RuntimeLoader.vue'

const route = useRoute()
const showFooter = ref(true)

watchEffect(() => {
  showFooter.value = route.name !== 'Terminal'
})
</script>

<template>
  <n-notification-provider>
    <runtime-loader />
  </n-notification-provider>
  <n-layout-header
    style="height: 42px"
    bordered
  >
    <beta-header />
  </n-layout-header>
  <n-layout
    position="absolute"
    :native-scrollbar="false"
    style="top: 42px"
    content-style="height: 100%; display: flex; flex-direction: column"
  >
    <n-layout-content :style="showFooter && {flex: '1 0 auto', backgroundColor: '#eee'}">
      <n-message-provider>
        <router-view v-slot="{ Component }">
          <keep-alive>
            <component :is="Component" />
          </keep-alive>
        </router-view>
      </n-message-provider>
    </n-layout-content>
    <n-back-top />
    <n-layout-footer
      v-if="showFooter"
      style="flex-shrink: 0"
    >
      <beta-footer />
    </n-layout-footer>
  </n-layout>
</template>

<style>
@import url(https://fonts.googleapis.com/css?family=Open+Sans:400);
@import url(https://fonts.googleapis.com/css?family=Droid+Sans+Mono);

body {
  font-family: "Open Sans", sans-serif;
}

ul,
h2,
h3,
h4,
label {
  margin: 0;
  padding: 0;
}

.fullscreen {
  position: fixed;
  left: 0;
  top: 0;
  right: 0;
  bottom: 0;
  z-index: 1000;
  overflow: auto;
}

.cell_output ul {
  list-style-type: none;
}

.card_actions {
  display: none;
  list-style-type: none;
  font-size: 0.75em;
}

.card_actions li {
  display: inline-block;
  border-bottom: 2px solid #ccc;
}

.foot {
  text-align: center;
  font-size: 90%;
}

/* Main page columns (saved and example queries) */

ul {
  list-style-type: none;
}

/* General styling */

h2 {
  padding: 10px 8px;
}

h3 {
  padding: 5px 8px;
}

p {
  padding: 0px 8px;
}

.collapsible > h2 {
  cursor: pointer;
  padding: 0;
  font-size: 1em;
  margin: 0.25em 0;
}

.collapsible > h2:before {
  content: "-";
}

.collapsible > h2.shown:before {
  content: "+";
}

/* Phones/mobile devices */
@media screen and (max-device-width: 767px) {
  .result_card {
    -webkit-box-shadow: none;
    box-shadow: none;
    border: 2px solid #ddd;
    border-radius: 2px;
    margin: 3px;
  }

  .example-group li {
    margin: 0.25em 0;
  }

  .example-group {
    -webkit-box-shadow: none;
    box-shadow: none;
    border: 1px solid #ccc;
  }

  .result,
  #footer {
    width: 100%;
    margin: 10px auto;
  }

  .graph {
    width: 100%;
    margin: 0 auto;
    padding: 0;
    border: 0;
  }

  .graph:hover {
    border: 0;
  }
}

/* Tablets and base for desktops */
@media screen and (min-device-width: 768px) {
  .result,
  #footer {
    width: 600px;
    margin: 10px auto;
  }
}

@media screen and (min-device-width: 1280px) {
  .fullscreen .steps {
    margin: 2em auto;
    width: 700px;
  }
}
</style>
