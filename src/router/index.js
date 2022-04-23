import { createRouter, createWebHistory } from 'vue-router'
import MainView from '@/views/MainView.vue'
import ResultView from '@/views/ResultView.vue'
import TerminalView from '@/views/TerminalView.vue'

const routes = [
  { path: '/', name: 'Main', component: MainView },
  { path: '/terminal', name: 'Terminal', component: TerminalView },
  { path: '/input/:expr', name: 'Result', component: ResultView }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
