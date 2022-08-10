// blocker: Firefox https://stackoverflow.com/questions/44118600/web-workers-how-to-import-modules
// import { pyodideURL, kernelVersion } from '/package.json'
const kernelName = 'sympy_beta_kernel'
const kernelVersion = '1.0.0'
const useDevSymPy = false

importScripts('https://cdn.jsdelivr.net/pyodide/v0.21.0/full/pyodide.js')

async function loadPyodideAndPackages () {
  let errorMsg
  const pkgs = ['micropip', 'docutils', 'matplotlib', 'numpy', 'nltk', 'typing-extensions', 'mpmath']
  self.pyodide = await loadPyodide()
  self.postMessage({ stage: 'PYODIDE_DOWNLOADED' })
  await self.pyodide.loadPackage(pkgs,
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
  const config = { kernelName, kernelVersion, useDevSymPy }
  self.pyodide.registerJsModule('config', config)
  await self.pyodide.runPythonAsync(`
    from pathlib import Path
    from config import kernelName, kernelVersion, useDevSymPy
    import micropip
    from pyodide.http import pyfetch
    if useDevSymPy:
        await micropip.install('/sympy-1.11.dev0-py3-none-any.whl')
    else:
        await micropip.install('sympy==1.11')
    words_res = await pyfetch('/words.zip')
    path = Path('/home/pyodide/nltk_data/corpora')
    path.mkdir(parents=True)
    with open(path/'words.zip', 'wb') as f:
        f.write(await words_res.bytes())
    await micropip.install([f'/{kernelName}-{kernelVersion}-py3-none-any.whl',
        'cplot',
        '/antlr4_python3_runtime-4.10-py3-none-any.whl'])
    from api import eval_input, eval_latex_input, eval_card as eval_card_inner, get_sympy_version
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
