<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { NSpin, NA } from 'naive-ui'
import { getPyodideVersion, getSymPyVersion } from '../workerAPI'
import { homepage } from '../../package.json'

const pyodideVersion = ref<string>()
const sympyVersion = ref<string>()
const commit = '__COMMIT__'
const commitURL = `${homepage}/commit/${commit}`
const buildDate = '__BUILD_DATE__'

onMounted(async () => {
  pyodideVersion.value = await getPyodideVersion()
  sympyVersion.value = await getSymPyVersion()
})
</script>

<template>
  <div id="footer">
    <p>
      Pyodide version
      <template v-if="pyodideVersion">
        {{ pyodideVersion }}
      </template>
      <n-spin
        v-else
        size="small"
      />
      ·
      SymPy version
      <template v-if="sympyVersion">
        {{ sympyVersion }}
      </template>
      <n-spin
        v-else
        size="small"
      />
      <br>
      Commit <n-a
        :href="commitURL"
        target="_blank"
      >
        {{ commit.slice(0, 7) }}
      </n-a> · Built at {{ buildDate }}
    </p>
    <p>
      &copy; 2013-2020 SymPy Development Team
      <br>&copy; 2021-2023 Qijia Liu
    </p>
    <p>
      This project is Free and Open Source (AGPLv3+):
      <n-a
        :href="homepage"
        target="_blank"
      >
        SymPy Beta on GitHub
      </n-a>.
    </p>
  </div>
</template>
