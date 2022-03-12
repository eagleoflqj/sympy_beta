// blocker: Firefox https://stackoverflow.com/questions/44118600/web-workers-how-to-import-modules
// import { pyodideURL, kernelVersion } from '/package.json'
const pyodideURL = 'https://cdn.jsdelivr.net/pyodide/v0.19.1/full/'
const kernelName = 'sympy_beta_kernel'
const kernelVersion = '1.0.0'

importScripts(`${pyodideURL}pyodide.js`)

async function loadPyodideAndPackages () {
  let errorMsg
  self.pyodide = await loadPyodide({
    indexURL: pyodideURL
  })
  self.postMessage({ stage: 'PYODIDE_DOWNLOADED' })
  await self.pyodide.loadPackage(['micropip', 'docutils', 'numpy', 'sympy'],
    console.log, msg => {
      console.error(msg)
      errorMsg = msg
    }
  )
  if (errorMsg) {
    self.postMessage({ errorMsg })
    throw new Error()
  }
  self.postMessage({ stage: 'PKG_DOWNLOADED' })
  const config = { kernelName, kernelVersion }
  self.pyodide.registerJsModule('config', config)
  await self.pyodide.runPythonAsync(`
    from config import kernelName, kernelVersion
    import micropip
    await micropip.install(f'/{kernelName}-{kernelVersion}-py3-none-any.whl')
    from api import eval_input, eval_card as eval_card_inner, get_sympy_version
    def eval_card(card_name, expression, variable, parameters):
        return eval_card_inner(card_name, expression, variable, parameters.to_py())
  `)
  self.postMessage({ stage: 'KERNEL_LOADED' })
}

const pyodideReadyPromise = loadPyodideAndPackages()

self.onmessage = async (event) => {
  await pyodideReadyPromise
  const { id, func, args } = event.data
  if (func === 'getPyodideVersion') {
    self.postMessage({ id, result: self.pyodide.version })
    return
  }
  const f = self.pyodide.globals.get(func)
  let result = f(...args)
  if (self.pyodide.isPyProxy(result)) {
    const tempResult = result
    result = result.toJs({ dict_converter: Object.fromEntries })
    tempResult.destroy()
  }
  self.postMessage({ id, result })
}
