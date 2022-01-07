<script setup>
import { NNotificationProvider, NLayout, NLayoutHeader, NBackTop } from 'naive-ui'
import BetaHeader from '@/components/BetaHeader.vue'
import BetaFooter from '@/components/BetaFooter.vue'
import RuntimeLoader from '@/components/RuntimeLoader.vue'
</script>

<template>
  <n-notification-provider>
    <runtime-loader />
  </n-notification-provider>
  <n-layout position="absolute">
    <n-layout-header
      style="height: 42px"
      bordered
    >
      <beta-header />
    </n-layout-header>
    <n-layout
      position="absolute"
      :native-scrollbar="false"
      style="top: 42px; background-color: #eee"
    >
      <router-view />
      <beta-footer />
      <n-back-top />
    </n-layout>
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

pre {
  font-family: "Droid Sans Mono", monospace;
}

h1 {
  font-family: "Gentium Basic", serif;
  font-weight: normal;
  color: #fff;
  margin: 0;
  line-height: 50px;
}

h1 a:link,
h1 a:visited,
h1 a:active {
  color: #fff;
  text-decoration: none;
}

h1 a:hover {
  color: #96c56f;
}

h1 a img {
  vertical-align: bottom;
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

.cell_output table {
  border-collapse: collapse;
  border: 1px solid #000;
  margin: auto;
}

.cell_output td,
.cell_output th {
  border: 1px solid #000;
  padding: 0.25em 0.5em;
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

.input {
  text-align: center;
  padding: 20px 0;
  background: #3b5526;
}

.input input[type="text"] {
  font-family: "Droid Sans Mono", monospace;
  text-align: left;
}

.foot {
  text-align: center;
  font-size: 90%;
}

/* Main page columns (saved and example queries) */

.main {
  line-height: 1.15em;
}

.main p {
  margin: 0;
  padding: 0;
}

.col h2 {
  text-align: center;
  font-size: 1.25em;
  font-weight: normal;
}

.col ul {
  list-style-type: none;
}

.col.recent li {
  margin: 0.5em 0;
  border-bottom: 1px solid #777;
}

.col.recent a:link,
.col.recent a:visited,
.col.recent a:hover,
.col.recent a:active {
  text-decoration: none;
  color: #3b5526;
  width: 70%;
  display: inline-block;
  font-family: "Droid Sans Mono", monospace;
}

.col.recent a.remove {
  width: auto;
  float: right;
  display: none;
}

.col.recent li:hover a.remove {
  display: block;
}

.col button a:link,
.col button a:visited,
.col button a:hover,
.col button a:active {
  color: #fff;
  text-decoration: none;
}

#clear-all-recent {
  font-size: 90%;
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

  .col {
    width: auto;
    margin: 10px 10px;
    font-size: 125%;
  }

  .col.recent a.remove {
    display: inline-block;
  }

  .col.example .example-group li {
    margin: 0.25em 0;
  }

  .col.example .example-group li > span {
    padding-top: 0.25em;
  }

  .col.example .example-group li > span:after {
    content: ":";
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

  .menu_right {
    display: inline;
  }

  #mobile-keyboard button {
    width: 2em;
    font-size: 1.25em;
    margin: 0;
  }
}

/* Tablets and base for desktops */
@media screen and (min-device-width: 768px) {
  .result,
  #footer {
    width: 600px;
    margin: 10px auto;
  }

  .main {
    width: 740px;
    margin: 10px auto;
  }

  .col {
    width: 360px;
  }

  .col.example {
    width: 720px;
  }

  .col.recent + .col.example {
    width: 360px;
  }

  .col.recent {
    float: left;
    height: 100%;
  }

  .col.recent a.remove {
    display: inline-block;
  }

  .col.example {
    margin: auto;
  }

  .col.recent ~ .col.example {
    float: right;
    height: 100%;
  }

  .col.example div.example-group li {
    margin: 0.25em 0;
  }

  .col.example .example-group li > span:after {
    content: ":";
  }

  .menu_right {
    float: right;
    display: block;
  }

  #mobile-keyboard button {
    width: 3em;
    font-size: 1.5em;
  }
}

@media screen and (min-device-width: 1280px) {
  .main {
    width: 800px;
    margin: 10px auto;
  }

  .col {
    width: 390px;
  }

  .col.example {
    width: 600px;
  }

  .col.recent + .col.example {
    width: 390px;
  }

  .col.example .example-group li {
    margin: 0;
  }

  .col.recent a.remove {
    display: none;
  }

  .fullscreen .steps {
    margin: 2em auto;
    width: 700px;
  }
}
</style>
