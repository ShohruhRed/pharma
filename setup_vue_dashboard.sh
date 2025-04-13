#!/bin/bash

# 1. Создание проекта через Vite
npm create vite@latest pharma-dashboard -- --template vue
cd pharma-dashboard

# 2. Установка зависимостей
npm install
npm install axios vue-router@4 chart.js vue-chartjs@4

# 3. Создание директорий
mkdir -p src/components
mkdir -p src/views
mkdir -p src/router
mkdir -p src/api

# 4. Создание файлов компонентов
touch src/components/BatchList.vue
touch src/components/StageTimeline.vue
touch src/components/SensorDataChart.vue
touch src/components/PredictionPanel.vue

# 5. Создание файлов для представлений
touch src/views/DashboardView.vue
touch src/views/PredictionsView.vue

# 6. Создание файлов роутера и API
cat <<EOF > src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'
import PredictionsView from '../views/PredictionsView.vue'

const routes = [
  { path: '/', component: DashboardView },
  { path: '/predictions', component: PredictionsView }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
EOF

cat <<EOF > src/api/index.js
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000',
})

export default api
EOF

# 7. Настройка main.js
cat <<EOF > src/main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

createApp(App).use(router).mount('#app')
EOF

# 8. Базовый App.vue
cat <<EOF > src/App.vue
<template>
  <router-view />
</template>
EOF

echo "✅ Vue проект pharma-dashboard создан и настроен!"
