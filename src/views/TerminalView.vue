<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { NSkeleton } from 'naive-ui'
import jQuery from 'jquery'
// @ts-ignore
import terminal from 'jquery.terminal'
import 'jquery.terminal/css/jquery.terminal.min.css'
import { LambdaWorker } from '@libreservice/my-worker'
import preExec from '../../kernel/gamma/pre_exec.py?raw'

terminal(window, jQuery)

let term: JQueryTerminal
const ps1 = '>>> '
const ps2 = '... '

const shellWorker = new LambdaWorker('/shellWorker.js')
const execute: (command: string) => Promise<void> = shellWorker.register('execute')
const complete: (arg: string) => Promise<string[]> = shellWorker.register('complete')
const keyboardInterrupt: () => Promise<void> = shellWorker.register('keyboardInterrupt')

const shellReadyPromise = new Promise(resolve => shellWorker.control('stage', resolve))
const loaded = ref(false)

shellWorker.control('setPrompt', (incomplete: boolean) => term.set_prompt(incomplete ? ps2 : ps1))
shellWorker.control('echo', (arg: string, option?: { newline: boolean }) => term.echo(arg, option))
shellWorker.control('error', (arg: string) => term.error(arg))

async function interpreter (command: string) {
  term.pause()
  await execute(command).catch((e: Error) => {
    term.error(e.message)
  })
  term.resume()
}

let pendingComplete = false

async function tabComplete (command: string) {
  if (pendingComplete) {
    throw Error()
  }
  pendingComplete = true
  return complete(command)
}

const container = ref<Element>()

onMounted(async () => {
  const banner = await shellReadyPromise
  term = jQuery(container.value!).terminal(interpreter, {
    greetings: `Welcome to the Pyodide terminal emulator 🐍\n${banner}`,
    prompt: ps1,
    completionEscape: false,
    completion: (command, callback) => {
      tabComplete(command).then(arg => {
        callback(arg)
        pendingComplete = false
      }).catch(() => {})
    },
    keymap: {
      'CTRL+C': async () => {
        keyboardInterrupt()
        term.enter()
        term.echo('KeyboardInterrupt')
        term.set_command('')
        term.set_prompt(ps1)
      },
      TAB: (event, original) => {
        const command = term.before_cursor()
        if (command.trim() === '') {
          term.insert('\t')
          return false
        }
        return original(event)
      }
    }
  })
  for (const command of preExec.split('\n').slice(0, -1)) {
    term.exec(command)
  }
  loaded.value = true
})
</script>

<template>
  <div
    ref="container"
    style="height: 100%; padding: 10px"
  >
    <template v-if="!loaded">
      <!-- eslint-disable vue/no-unused-vars -->
      <n-skeleton
        v-for="i in 43"
        text
        width="10.833px"
      />
      <br>
      <n-skeleton
        v-for="i in 62"
        text
        width="10.833px"
      />
      <br>
      <n-skeleton
        v-for="i in 70"
        text
        width="10.833px"
      />
      <!-- eslint-enable vue/no-unused-vars -->
    </template>
  </div>
</template>

<style>
.terminal {
  --size: 1.5;
  --color: rgba(255, 255, 255, 0.8);
}
</style>
