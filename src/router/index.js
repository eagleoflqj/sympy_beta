import { createRouter, createWebHistory } from 'vue-router'
import Main from '@/views/Main.vue'
import Result from '@/views/Result.vue'

const routes = [
  { path: '/', name: 'Main', component: Main },
  { path: '/input/:expr', name: 'Result', component: Result }
]

const router = createRouter({
  history: createWebHistory(),
  routes: routes
})

export default router
