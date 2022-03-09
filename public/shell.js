const pyodideURL = 'https://cdn.jsdelivr.net/pyodide/v0.19.1/full/'

importScripts(`${pyodideURL}pyodide.js`)

let awaitFut = null
let pyconsole = null
let reprShorten = null
let clearConsole = null

async function loadPyodideAndPackages () {
  self.pyodide = await loadPyodide({
    indexURL: pyodideURL
  })
  await self.pyodide.loadPackage(['micropip', 'sympy'])
  const namespace = self.pyodide.globals.get('dict')()
  await self.pyodide.runPythonAsync(`
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
  `, namespace)
  reprShorten = namespace.get('repr_shorten')
  self.postMessage({ type: 'ready', arg: namespace.get('BANNER') })
  awaitFut = namespace.get('await_fut')
  pyconsole = namespace.get('pyconsole')
  pyconsole.stdout_callback = s => self.postMessage({ type: 'echo', args: [s, { newline: false }] })
  pyconsole.stderr_callback = s => self.postMessage({ type: 'error', arg: s.trimEnd() })
  clearConsole = namespace.get('clear_console')
  namespace.destroy()
}

const pyodideReadyPromise = loadPyodideAndPackages()

self.onmessage = async event => {
  await pyodideReadyPromise
  const { data } = event
  switch (data.type) {
    case 'exec':
      for (const line of data.arg.split('\n')) {
        const fut = pyconsole.push(line)
        self.postMessage({ type: 'set_prompt', arg: fut.syntax_check === 'incomplete' })
        switch (fut.syntax_check) {
          case 'syntax-error':
            self.postMessage({ type: 'error', arg: fut.formatted_error.trimEnd() })
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
            self.postMessage({
              type: 'echo',
              args: [reprShorten.callKwargs(value, {
                separator: '\n[[;orange;]<long output truncated>]\n'
              })]
            })
          }
          if (self.pyodide.isPyProxy(value)) {
            value.destroy()
          }
        } catch (e) {
          if (e.constructor.name === 'PythonError') {
            const message = fut.formatted_error || e.message
            self.postMessage({ type: 'error', arg: message.trimEnd() })
          } else {
            throw e
          }
        } finally {
          fut.destroy()
          wrapped.destroy()
        }
      }
      self.postMessage({ type: 'resume' })
      break
    case 'complete':
      self.postMessage({ type: 'complete', arg: pyconsole.complete(data.arg).toJs()[0] })
      break
    case 'clear':
      clearConsole()
      break
  }
}
