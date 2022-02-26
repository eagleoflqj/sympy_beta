// blocker: Firefox https://stackoverflow.com/questions/44118600/web-workers-how-to-import-modules
// import { pyodideURL, kernelVersion } from '/package.json'
const pyodideURL = 'https://cdn.jsdelivr.net/pyodide/v0.19.0/full/'
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
    import traceback
    from config import kernelName, kernelVersion
    import micropip
    await micropip.install(f'/{kernelName}-{kernelVersion}-py3-none-any.whl')
    from gamma.logic import SymPyGamma
    sympy_gamma = SymPyGamma()
    def getSymPyVersion():
      from sympy import __version__
      return __version__
    def ev(expression, variable):
        return sympy_gamma.eval(expression, variable)
    def evcd(a, b, c, d):
        try:
            return sympy_gamma.eval_card(a, b, c, d.to_py())
        except ValueError as e:
            return {'error': str(e)}
        except Exception as e:
            trace = traceback.format_exc()
            return {
                'error': ('There was an error in Gamma. For reference '
                        'the last five traceback entries are: ' + trace)
            }
  `)
  self.postMessage({ stage: 'KERNEL_LOADED' })
}

const pyodideReadyPromise = loadPyodideAndPackages()

self.onmessage = async (event) => {
  await pyodideReadyPromise
  const { id, func, args } = event.data
  try {
    if (func === 'getPyodideVersion') {
      self.postMessage({ id, result: self.pyodide.version })
      return
    }
    const f = self.pyodide.globals.get(func)
    const tempResult = f(...args)
    if (self.pyodide.isPyProxy(tempResult)) {
      const result = tempResult.toJs({ dict_converter: Object.fromEntries })
      tempResult.destroy()
      self.postMessage({ id, result })
    } else {
      self.postMessage({ id, result: tempResult })
    }
  } catch (error) {
    self.postMessage({ error: error.message })
  }
}
