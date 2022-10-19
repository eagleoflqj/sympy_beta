import { exit } from 'process'
import { execSync } from 'child_process'
import os from 'os'

const SOURCE_DATE_EPOCH = 315532800

const encoding = 'utf-8'

function ensure (result, message) {
  if (result.status === 0) {
    return
  }
  console.error(message)
  console.log('------stdout------')
  console.log(result.stdout)
  console.log('------stderr------')
  console.error(result.stderr)
  exit(1)
}

// copy from https://github.com/antfu/ni/blob/main/src/utils.ts#L17
function cmdExists (cmd) {
  try {
    execSync(
      os.platform() === 'win32'
        ? `cmd /c "(help ${cmd} > nul || exit 0) && where ${cmd} > nul 2> nul"`
        : `command -v ${cmd}`
    )
    return true
  } catch {
    return false
  }
}

const python = cmdExists('python3') ? 'python3' : 'python'

export { SOURCE_DATE_EPOCH, encoding, ensure, cmdExists, python }
