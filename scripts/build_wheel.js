const { spawn } = require('child_process')
const { rename } = require('fs')
const { exit } = require('process')
const { kernelName, kernelVersion } = require('../package.json')
process.chdir('kernel')
const child = spawn('python3', ['setup.py', 'bdist_wheel'],
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
