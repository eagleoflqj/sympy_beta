import { spawn } from 'child_process'
import { rename, readFileSync } from 'fs'
import { chdir, exit } from 'process'

const { kernelName, kernelVersion } = JSON.parse(readFileSync('package.json'))
chdir('kernel')
const child = spawn('python', ['setup.py', 'bdist_wheel'],
  { env: { ...process.env, SOURCE_DATE_EPOCH: 315532800 } })
child.on('exit', code => {
  if (code !== 0) {
    console.error('Fail to build wheel.')
    exit(code)
  }
  const wheel = `${kernelName}-${kernelVersion}-py3-none-any.whl`
  rename(`dist/${wheel}`, `../public/${wheel}`,
    err => err && console.log(err))
})
