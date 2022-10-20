import { expose, control } from '@libreservice/my-worker'
import { pyodideURL } from '../package.json'

importScripts(pyodideURL)

let pyodide: any
declare const loadPyodide: () => Promise<any>

let awaitFut: any
let pyconsole: any
let reprShorten: any
let clearConsole: () => void

const stage: (banner: string) => void = control('stage')
const setPrompt: (incomplete: boolean) => void = control('setPrompt')
const echo: (arg: string, option?: { newline: boolean }) => void = control('echo')
const error: (arg: string) => void = control('error')

async function loadPyodideAndPackages () {
  pyodide = await loadPyodide()
  await pyodide.loadPackage(['micropip'])
  const namespace = pyodide.globals.get('dict')()
  await pyodide.runPythonAsync(`
    import micropip
    await micropip.install('sympy==1.11')
    import sys
    from pyodide import to_js
    from pyodide.console import PyodideConsole, repr_shorten, BANNER
    import __main__
    pyconsole = PyodideConsole(__main__.__dict__)
    import builtins
    async def await_fut(fut):
        res = await fut
        if res is not None:
            builtins._ = res
        return to_js([res], depth=1)
    def clear_console():
        pyconsole.buffer = []
  `, { globals: namespace })
  reprShorten = namespace.get('repr_shorten')
  stage(namespace.get('BANNER'))
  awaitFut = namespace.get('await_fut')
  pyconsole = namespace.get('pyconsole')
  pyconsole.stdout_callback = (s: string) => echo(s, { newline: false })
  pyconsole.stderr_callback = (s: string) => error(s.trimEnd())
  clearConsole = namespace.get('clear_console')
  namespace.destroy()
}

const pyodideReadyPromise = loadPyodideAndPackages()

async function execute (command: string) {
  for (const line of command.split('\n')) {
    const fut = pyconsole.push(line)
    setPrompt(fut.syntax_check === 'incomplete')
    switch (fut.syntax_check) {
      case 'syntax-error':
        error(fut.formatted_error.trimEnd())
        continue
      case 'incomplete':
        continue
      case 'complete':
        break
      default:
        throw new Error(`Unexpected type ${fut.syntax_check}`)
    }
    const wrapped = awaitFut(fut)
    try {
      const [value] = await wrapped
      if (value !== undefined) {
        echo(reprShorten.callKwargs(value, {
          separator: '\n[[;orange;]<long output truncated>]\n'
        }))
      }
      if (pyodide.isPyProxy(value)) {
        value.destroy()
      }
    } catch (e: any) {
      if (e.constructor.name === 'PythonError') {
        const message = fut.formatted_error || e.message
        error(message.trimEnd())
      }
    } finally {
      fut.destroy()
      wrapped.destroy()
    }
  }
}

function complete (arg: string): string[] {
  return pyconsole.complete(arg).toJs()[0]
}

function keyboardInterrupt () {
  return clearConsole() // dynamic binding after pyodide loaded
}

expose({ execute, complete, keyboardInterrupt }, pyodideReadyPromise)
