import { LambdaWorker } from '@libreservice/my-worker'

const pyodideWorker = new LambdaWorker('/pyodideWorker.js')

type StageCallback = (arg: { stage: string, errorMsg?: string }) => void

function registerStageCallback (arg: StageCallback) {
  pyodideWorker.control('stage', arg)
}

const evalInput: (input: string, variable?: string) => Promise<{
  result: InputResult[]
  error: string
}> = pyodideWorker.register('evalInput')

const evalLatexInput: (input: string) => Promise<{
  result: string
  error: string
}> = pyodideWorker.register('evalLatexInput')

const evalCard = pyodideWorker.register('evalCard')

const getPyodideVersion: () => Promise<string> = pyodideWorker.register('getPyodideVersion')

const getSymPyVersion: () => Promise<string> = pyodideWorker.register('getSymPyVersion')

export { evalInput, evalLatexInput, evalCard, getPyodideVersion, getSymPyVersion, registerStageCallback }
