<script setup>
import { register } from '@/js/workerAPI.js'
import { useNotification } from 'naive-ui'

const notification = useNotification()
let loaded = false

function notifyLoading () {
  let baseContent = 'Downloading Pyodide'
  let count = 1
  const reactive = notification.create({
    type: 'info',
    title: 'Setting up runtime',
    content: baseContent + ' ' + '.'.repeat(count),
    onAfterEnter: () => {
      const plusCount = () => {
        count = count % 3 + 1
        reactive.content = baseContent + ' ' + '.'.repeat(count)
        loaded || setTimeout(plusCount, 500)
      }
      setTimeout(plusCount, 500)
    }
  })
  return {
    setContent: function (newContent) {
      baseContent = newContent
    },
    destroy: () => reactive.destroy()
  }
}

function notifyLoaded () {
  notification.create({
    type: 'success',
    title: 'Runtime is ready',
    content: 'All computation is in your browser.',
    duration: 3000,
    closable: true
  })
}

function notifyError (errorMsg) {
  notification.create({
    type: 'error',
    title: 'An error occurs',
    content: `${errorMsg}\nPlease check your network and refresh.`,
    closable: true
  })
}

const loadingNotification = notifyLoading()

register(({ stage, errorMsg }) => {
  switch (stage) {
    case 'PYODIDE_DOWNLOADED':
      loadingNotification.setContent('Downloading packages')
      break
    case 'PKG_DOWNLOADED':
      loadingNotification.setContent('Loading kernel')
      break
    case 'KERNEL_LOADED':
      loadingNotification.destroy()
      notifyLoaded()
      loaded = true
      break
    default:
      loadingNotification.destroy()
      notifyError(errorMsg)
  }
})
</script>
