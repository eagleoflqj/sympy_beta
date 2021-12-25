// blocker: Firefox https://stackoverflow.com/questions/44118600/web-workers-how-to-import-modules
// import { pyodideURL, gammaVersion } from '/package.json'
const pyodideURL = 'https://cdn.jsdelivr.net/pyodide/v0.18.1/full/'
const gammaVersion = '1.0.0'

importScripts(`${pyodideURL}pyodide.js`)

async function loadPyodideAndPackages() {
  self.pyodide = await loadPyodide({
    indexURL: pyodideURL,
  })
  self.postMessage({ id: -1 })
  await self.pyodide.loadPackage(["micropip", "docutils", "numpy", "sympy"])
  self.postMessage({ id: -2 })
  const config = { gammaVersion }
  pyodide.registerJsModule("config", config)
  await self.pyodide.runPythonAsync(`
    import traceback
    from config import gammaVersion
    import micropip
    await micropip.install(f'/gamma-{gammaVersion}-py3-none-any.whl')
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
  self.postMessage({ id: -3 })
}

let pyodideReadyPromise = loadPyodideAndPackages()

self.onmessage = async (event) => {
  await pyodideReadyPromise
  const { id, func, args } = event.data
  try {
    f = self.pyodide.globals.get(func)
    temp_result = f(...args)
    if (pyodide.isPyProxy(temp_result)) {
      const result = temp_result.toJs({ dict_converter: Object.fromEntries })
      temp_result.destroy()
      self.postMessage({ id, result })
    } else {
      self.postMessage({ id, result: temp_result})
    }
  } catch (error) {
    self.postMessage({ error: error.message })
  }
}
