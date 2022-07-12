import { spawnSync } from 'child_process'
import { rename, readFileSync } from 'fs'
import { chdir } from 'process'
import { SOURCE_DATE_EPOCH, encoding, ensure } from './util.mjs'

console.log('Start build_wheel.mjs.')

const { kernelName, kernelVersion } = JSON.parse(readFileSync('package.json'))
chdir('kernel')

ensure(spawnSync('python', ['setup.py', 'bdist_wheel'],
  { encoding, env: { ...process.env, SOURCE_DATE_EPOCH } }))

const wheel = `${kernelName}-${kernelVersion}-py3-none-any.whl`
rename(`dist/${wheel}`, `../public/${wheel}`,
  err => err && console.log(err))

console.log('Finish build_wheel.mjs.')
