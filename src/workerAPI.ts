const pyodideWorker = new Worker('/worker.js')

const resolves: { [key: number]: (arg: any) => void } = {}

type StageCallback = (arg: { stage: string, errorMsg?: string }) => void
let stageCallback: StageCallback

const register: (arg: StageCallback) => void = arg => {
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
  return (func: string) => function (...args: any[]) {
    id = (id + 1) % Number.MAX_SAFE_INTEGER
    return new Promise<any>(resolve => {
      resolves[id] = resolve
      pyodideWorker.postMessage({ id, func, args })
    })
  }
})()

const evalInput: (input: string, variable?: string) => Promise<{
  result: InputResult[]
  error: string
}> = wrapper('eval_input')
const evalLatexInput: (input: string) => Promise<{
  result: string
  error: string
}> = wrapper('eval_latex_input')
const evalCard = wrapper('eval_card')
const getPyodideVersion: () => Promise<string> = wrapper('getPyodideVersion')
const getSymPyVersion = wrapper('get_sympy_version')

export { evalInput, evalLatexInput, evalCard, register, getPyodideVersion, getSymPyVersion }
