<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="6" lg="3" v-for="(item, index) in stats" :key="index">
        <v-card :color="item.color" class="pa-4 text-white" elevation="5" rounded="xl">
          <v-card-title class="d-flex align-center justify-space-between">
            <span>{{ item.title }}</span>
            <v-icon size="28">{{ item.icon }}</v-icon>
          </v-card-title>
          <v-card-text class="text-h4 font-weight-bold">
            {{ item.value }}
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import {
  fetchBatches,
  fetchStagesByBatch,
  fetchSensorDataByStage,
  fetchPredictionByStage,
} from '@/api'

export default {
  name: 'DashboardView',
  data() {
    return {
      batches: [],
      stages: [],
      sensorData: [],
      predictions: [],
    }
  },
  computed: {
    stats() {
      return [
        {
          title: 'Partiyalar soni',
          value: this.batches.length || '...',
          icon: 'mdi-package-variant-closed',
          color: 'indigo',
        },
        {
          title: 'Oxirgi harorat',
          value: this.sensorData.length
            ? `${this.sensorData.at(-1).temperature}°C`
            : '...',
          icon: 'mdi-thermometer',
          color: 'deep-orange',
        },
        {
          title: 'Bashoratlar',
          value: this.predictions.length || '...',
          icon: 'mdi-brain',
          color: 'teal',
        },
        {
          title: 'Risk darajasi',
          value: this.predictions.length
            ? this.predictions.at(-1).risk_level
            : '...',
          icon: 'mdi-alert-circle',
          color: 'red darken-1',
        },
      ]
    },
  },
  async mounted() {
    try {
      this.batches = await fetchBatches()
      const latestBatch = this.batches.at(-1)
      if (!latestBatch) return

      this.stages = await fetchStagesByBatch(latestBatch.id)
      const latestStage = this.stages.at(-1)
      if (!latestStage) return

      this.sensorData = await fetchSensorDataByStage(latestStage.id)
      this.predictions = await fetchPredictionByStage(latestStage.id)

      console.log('✅ Ma’lumotlar yuklandi')
    } catch (e) {
      console.error('❌ Yuklashda xatolik:', e)
    }
  },
}
</script>
