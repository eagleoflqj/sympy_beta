<script setup>
import { ref, onMounted } from 'vue'
import { NSpin, NA } from 'naive-ui'
import { getPyodideVersion, getSymPyVersion } from '@/js/workerAPI.js'
import { homepage } from '@/../package.json'

const pyodideVersion = ref(null)
const sympyVersion = ref(null)

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
    </p>
    <p>
      &copy; 2013-2020 SymPy Development Team
      <br>&copy; 2021-2022 Qijia Liu
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
