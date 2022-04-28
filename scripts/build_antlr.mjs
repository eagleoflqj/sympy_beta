import { spawnSync } from 'child_process'
import { renameSync, readFileSync, writeFileSync } from 'fs'
import { chdir, exit } from 'process'

const { status } = spawnSync('pip', ['download', 'antlr4-python3-runtime==4.7'])
if (status !== 0) {
  console.error('Fail to download antlr4.')
  exit(status)
}

spawnSync('tar', ['xzf', 'antlr4-python3-runtime-4.7.tar.gz'])
chdir('antlr4-python3-runtime-4.7')
const inStr = readFileSync('setup.py', { encoding: 'utf-8' })
const outStr = inStr.replace('distutils.core', 'setuptools')
writeFileSync('setup.py', outStr)
spawnSync('python', ['setup.py', 'bdist_wheel'],
  { env: { ...process.env, SOURCE_DATE_EPOCH: 315532800 } })
const wheel = 'antlr4_python3_runtime-4.7-py3-none-any.whl'
renameSync(`dist/${wheel}`, `../public/${wheel}`)
