<script setup>
import { register } from '@/js/workerAPI.js'
import { useNotification } from 'naive-ui'

const notification = useNotification()

function notifyLoading () {
  let baseContent = 'Downloading Pyodide'
  let count = 1
  const reactive = notification.create({
    type: 'info',
    title: 'Setting up runtime',
    content: baseContent + ' ' + '.'.repeat(count),
    closable: false,
    onAfterEnter: () => {
      const plusCount = () => {
        count = count % 3 + 1
        reactive.content = baseContent + ' ' + '.'.repeat(count)
        setTimeout(plusCount, 500)
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

const loadingNotification = notifyLoading()

register((id) => {
  switch (id) {
    case -1:
      loadingNotification.setContent('Downloading packages')
      break
    case -2:
      loadingNotification.setContent('Loading kernel')
      break
    case -3:
      loadingNotification.destroy()
      notifyLoaded()
      break
  }
})
</script>
