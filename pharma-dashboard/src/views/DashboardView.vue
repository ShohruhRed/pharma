<template>
  <v-container fluid>
    <!-- === KPI-карточки === -->
    <v-row dense>
      <!-- 1) Partiyalar soni -->
      <v-col cols="12" md="6" lg="3" v-for="(card, i) in statsCards" :key="i">
        <v-card
          :color="card.color"
          class="pa-4 text-white"
          elevation="5"
          rounded="xl"
        >
          <v-card-title class="d-flex align-center justify-space-between">
            <span>{{ card.title }}</span>
            <v-icon size="28">{{ card.icon }}</v-icon>
          </v-card-title>
          <v-card-text class="text-h4 font-weight-bold">
            {{ card.value }}
          </v-card-text>
        </v-card>
      </v-col>

      <!-- 3) Holat (по последнему этапу последней партии) -->
      <v-col cols="12" md="6" lg="3">
        <v-card
          :color="statusCard.color"
          class="pa-4 text-white"
          elevation="5"
          rounded="xl"
        >
          <v-card-title class="d-flex align-center">
            <v-icon size="28" class="me-2">{{ statusCard.icon }}</v-icon>
            <span class="text-h6">Holat</span>
          </v-card-title>
          <v-card-text>
            <div class="text-h5 font-weight-bold">
              {{ statusCard.recommendation }}
            </div>
            <div class="subtitle-2">
              Ehtimollik: {{ statusCard.probability }}
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- === Аналитика: общая дефективность за всё время === -->
    <v-row dense class="mt-8">
      <v-col cols="12" md="6" lg="3">
        <v-card
          color="purple"
          class="pa-4 text-white"
          elevation="5"
          rounded="xl"
        >
          <v-card-title class="d-flex align-center justify-space-between">
            <span>Umumiy defekt darajasi</span>
            <v-icon size="28">mdi-chart-donut</v-icon>
          </v-card-title>
          <v-card-text class="text-h4 font-weight-bold">
            {{ overallDefectRate }}%
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- === Аналитика: дефективность по этапам за всё время === -->
    <v-row dense class="mt-4">
      <v-col
        v-for="stat in stageDefectRates"
        :key="stat.stage_idx"
        cols="12" sm="6" md="4" lg="2"
      >
        <v-card
          color="teal"
          class="pa-4 text-white"
          elevation="3"
          rounded="xl"
        >
          <v-card-title class="d-flex align-center justify-space-between">
            <span>{{ stat.stage_label }}</span>
            <v-icon size="20">mdi-chart-bar</v-icon>
          </v-card-title>
          <v-card-text class="text-h5 font-weight-bold">
            {{ stat.rate }}%
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import {
  fetchBatches,
  fetchStagesByBatch,
  fetchSensorDataByStage,
  fetchPredictionByStage,
  fetchAllPredictions
} from '@/api'

// ——— реактивные состояния ———
const batches          = ref([])
const stages           = ref([])
const sensorData       = ref([])
const latestPrediction = ref({})
const allPredictions   = ref([])  // ВСЕ предсказания за всё время

// ——— KPI-карты ———
const statsCards = computed(() => [
  {
    title: 'Partiyalar soni',
    value: batches.value.length,
    icon:  'mdi-package-variant-closed',
    color: 'indigo'
  },
  {
    title: 'Oxirgi harorat',
    value: sensorData.value.length
      ? `${sensorData.value.at(-1).temperature}°C`
      : '...',
    icon:  'mdi-thermometer',
    color: 'deep-orange'
  }
])

const statusCard = computed(() => {
  const rec  = latestPrediction.value.recommendation || '—'
  const prob = latestPrediction.value.defect_probability != null
    ? `${(latestPrediction.value.defect_probability * 100).toFixed(1)}%`
    : '—'
  const risk = latestPrediction.value.risk_level

  let color = 'teal', icon = 'mdi-help-circle'
  if (risk === 'high')   { color = 'red darken-1';    icon = 'mdi-alert-circle' }
  if (risk === 'medium') { color = 'orange darken-1'; icon = 'mdi-alert' }
  if (risk === 'low')    { color = 'green darken-1';  icon = 'mdi-check-circle' }

  return { recommendation: rec, probability: prob, color, icon }
})

// ——— Общая % дефективности за всё время ———
const overallDefectRate = computed(() => {
  const arr = allPredictions.value
  if (!arr.length) return '0.0'
  const bad = arr.filter(p => p.risk_level !== 'low').length
  return ((bad / arr.length) * 100).toFixed(1)
})

// ——— % дефективности по этапам (stage_idx 0…5) за всё время ———
const STAGE_LABELS = {
  0: 'Mixing',
  1: 'Granulation',
  2: 'Drying',
  3: 'Pressing',
  4: 'Coating',
  5: 'Packaging'
}
const stageDefectRates = computed(() => {
   // stages.value — это этапы, которые вы уже загрузили (у каждого есть id и stage_label)
  return stages.value.map(stage => {
   // группируем предсказания всех партий по совпадению stage_id
   const preds = allPredictions.value.filter(p => p.stage_id === stage.id)
   const total = preds.length
   const bad   = preds.filter(p => p.risk_level !== 'low').length
     return {
       stage_idx:   stage.stage_idx ?? stage.id,       // можно взять stage_idx если есть
       stage_label: stage.stage_label || stage.name,  
       rate:        total ? ((bad/total)*100).toFixed(1) : '0.0'
     }
   })
})

// ——— Загрузка данных ———
onMounted(async () => {
  // 1) все партии
  batches.value = await fetchBatches()

  // 2) этапы последней партии (для KPI-подблока)
  const batch = batches.value.at(0)
  if (batch) {
    stages.value = await fetchStagesByBatch(batch.id)
    const lastStage = stages.value.at(-1)
    if (lastStage) {
      sensorData.value = await fetchSensorDataByStage(lastStage.id)
      const lp = await fetchPredictionByStage(lastStage.id)
      latestPrediction.value = Array.isArray(lp) ? lp.at(-1) || {} : lp || {}
    }
  }

  // 3) ВСЕ предсказания за всё время для аналитики
  allPredictions.value = await fetchAllPredictions()
})
</script>

<style scoped>
.v-row.mt-8 { margin-top: 32px; }
.v-row.mt-4 { margin-top: 16px; }
</style>
