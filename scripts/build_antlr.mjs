import { spawnSync } from 'child_process'
import { renameSync, readFileSync, writeFileSync } from 'fs'
import { chdir } from 'process'
import { SOURCE_DATE_EPOCH, ensure, encoding } from './util.mjs'

console.log('Start build_antlr.mjs.')

ensure(spawnSync('pip', ['download', 'antlr4-python3-runtime==4.7'], { encoding }), 'Fail to download antlr4.')

ensure(spawnSync('tar', ['xzf', 'antlr4-python3-runtime-4.7.tar.gz'], { encoding }), 'Fail to extract antlr4.')

chdir('antlr4-python3-runtime-4.7')

const inStr = readFileSync('setup.py', { encoding })
const outStr = inStr.replace('distutils.core', 'setuptools')
writeFileSync('setup.py', outStr)

ensure(spawnSync('python', ['setup.py', 'bdist_wheel'],
  { encoding, env: { ...process.env, SOURCE_DATE_EPOCH } }), 'Fail to build antlr4.')

const wheel = 'antlr4_python3_runtime-4.7-py3-none-any.whl'
renameSync(`dist/${wheel}`, `../public/${wheel}`)

console.log('Finish build_antlr.mjs.')
