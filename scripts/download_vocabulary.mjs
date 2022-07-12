import { get } from 'https'
import { createWriteStream } from 'fs'
import { exit } from 'process'

console.log('Start download_vocabulary.mjs.')
get('https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/words.zip', response => {
  const { statusCode } = response
  if (statusCode !== 200) {
    console.error(`Fail to download vocabulary: status code ${statusCode}.`)
    exit(1)
  }
  console.log('Vocabulary downloaded.')
  const file = createWriteStream('public/words.zip')
  response.pipe(file)
  file.on('finish', () => {
    file.close()
    console.log('Finish download_vocabulary.mjs.')
  })
})
