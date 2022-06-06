import { exit } from 'process'

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

export { SOURCE_DATE_EPOCH, encoding, ensure }
