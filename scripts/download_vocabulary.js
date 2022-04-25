const http = require('https')
const fs = require('fs')
const { exit } = require('process')

http.get('https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/words.zip', response => {
  if (response.statusCode !== 200) {
    console.error('Fail to download vocabulary.')
    exit(1)
  }
  const file = fs.createWriteStream('public/words.zip')
  response.pipe(file)
  file.on('finish', () => {
    file.close()
  })
})
