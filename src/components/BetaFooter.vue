<script setup>
import { ref, onMounted } from 'vue'
import { NSpin } from 'naive-ui'
import { getSymPyVersion } from '@/js/workerAPI.js'

const sympyVersion = ref(null)

onMounted(async () => {
  sympyVersion.value = await getSymPyVersion()
})
</script>

<template>
  <div id="footer">
    <p>
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
      <a
        href="https://github.com/eagleoflqj/sympy_beta/"
        target="_blank"
      >SymPy Beta on GitHub</a>.
    </p>
  </div>
</template>
