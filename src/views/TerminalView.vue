<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { NSkeleton } from 'naive-ui'
import jQuery from 'jquery'
// @ts-ignore
import terminal from 'jquery.terminal'
import 'jquery.terminal/css/jquery.terminal.min.css'
import preExec from '../../kernel/gamma/pre_exec.py?raw'

terminal(window, jQuery)

let term: JQueryTerminal
const ps1 = '>>> '
const ps2 = '... '

let unlock: () => void
let res: () => void
let termReady: Promise<any> | null

async function lock () {
  const ready = termReady
  termReady = new Promise<void>(resolve => (res = resolve))
  await ready
  return res
}

const shellWorker = new Worker('/shell.js')
let shellReadyResolve: (arg: string) => void
const shellReadyPromise = new Promise(resolve => (shellReadyResolve = resolve))
const loaded = ref(false)

async function interpreter (command: string) {
  unlock = await lock()
  shellWorker.postMessage({ type: 'exec', arg: command })
  term.pause()
}

let completeResolve: ((arg: string[]) => void) | null = null

function complete (command: string) {
  return new Promise<string[]>((resolve, reject) => {
    if (completeResolve !== null) {
      reject(new Error())
    }
    completeResolve = resolve
    shellWorker.postMessage({ type: 'complete', arg: command })
  })
}

type Data = {
  type: 'set_prompt'
  arg: boolean
} | {
  type: 'error' | 'ready'
  arg: string
} | {
  type: 'echo'
  arg: string
  option?: object
} | {
  type: 'resume'
} | {
  type: 'complete'
  arg: string[]
}

shellWorker.onmessage = (msg: MessageEvent<Data>) => {
  const { data } = msg
  switch (data.type) {
    case 'set_prompt':
      term.set_prompt(data.arg ? ps2 : ps1)
      break
    case 'error':
      term.error(data.arg)
      break
    case 'echo':
      term.echo(data.arg, data.option)
      break
    case 'resume':
      term.resume()
      unlock()
      break
    case 'complete':
      completeResolve!(data.arg)
      completeResolve = null
      break
    case 'ready':
      shellReadyResolve(data.arg)
      break
  }
}

const container = ref<Element>()

onMounted(async () => {
  const banner = await shellReadyPromise
  term = jQuery(container.value!).terminal(interpreter, {
    greetings: `Welcome to the Pyodide terminal emulator 🐍\n${banner}`,
    prompt: ps1,
    completionEscape: false,
    completion: (command, callback) => {
      complete(command).then(callback).catch(() => {})
    },
    keymap: {
      'CTRL+C': async () => {
        shellWorker.postMessage({ type: 'clear' })
        term.enter('')
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
