const pyodideWorker = new Worker('/worker.js')

const resolves = {}

let stageCallback

const register = arg => {
  stageCallback = arg
}

pyodideWorker.onmessage = msg => {
  const { id, result, stage, errorMsg } = msg.data
  if (id !== undefined) {
    const resolve = resolves[id]
    delete resolves[id]
    resolve(result)
  } else {
    stageCallback({ stage, errorMsg })
  }
}

const wrapper = (() => {
  let id = -1
  return (func) => function (...args) {
    id = (id + 1) % Number.MAX_SAFE_INTEGER
    return new Promise((resolve, reject) => {
      resolves[id] = resolve
      pyodideWorker.postMessage({ id, func, args })
    })
  }
})()

const evalInput = wrapper('eval_input')
const evalCard = wrapper('eval_card')
const getPyodideVersion = wrapper('getPyodideVersion')
const getSymPyVersion = wrapper('get_sympy_version')

export { evalInput, evalCard, register, getPyodideVersion, getSymPyVersion }
