import { createRouter, createWebHistory } from 'vue-router'
import Main from '@/views/Main.vue'
import Result from '@/views/Result.vue'
import Terminal from '@/views/Terminal.vue'

const routes = [
  { path: '/', name: 'Main', component: Main },
  { path: '/terminal', name: 'Terminal', component: Terminal },
  { path: '/input/:expr', name: 'Result', component: Result }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
