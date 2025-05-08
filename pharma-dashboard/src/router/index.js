import { createRouter, createWebHistory } from 'vue-router'

const DashboardView   = () => import('@/views/DashboardView.vue')
const PredictionsView = () => import('@/views/PredictionsView.vue')
const SensorView = () => import('@/views/SensorView.vue')
const BatchesView = () => import('@/views/BatchesView.vue')
const OperatorView = () => import('@/views/OperatorView.vue')

const routes = [
  { path: '/', redirect: '/dashboard' },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashboardView,
  },
  {
    path: '/predictions',
    name: 'Predictions',
    component: PredictionsView,
  },
  { path: '/sensors', 
    name: 'Sensors', 
    component: SensorView 
  },
  { path: '/batches', 
    component: BatchesView 
  }, // <-- вот это добавь
  { path: '/operator', 
    component: OperatorView 
  },

]

export default createRouter({
  history: createWebHistory(),
  routes
})
