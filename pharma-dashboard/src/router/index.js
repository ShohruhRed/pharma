import { createRouter, createWebHistory } from 'vue-router'

const DashboardView   = () => import('@/views/DashboardView.vue')
const PredictionsView = () => import('@/views/PredictionsView.vue')

const routes = [
  { path: '/',           redirect: '/dashboard' },
  { path: '/dashboard',  component: DashboardView },
  { path: '/predictions', component: PredictionsView },
]

export default createRouter({
  history: createWebHistory(),
  routes
})
