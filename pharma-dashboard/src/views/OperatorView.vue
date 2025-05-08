<template>
  <v-container>
    <!-- Информация о партии и этапе -->
    <v-row>
      <v-col cols="12">
        <v-alert type="info" class="mb-4">
          Partiya: <strong>{{ batchName }}</strong> |
          Etap: <strong>{{ stageName }}</strong>
        </v-alert>
      </v-col>
    </v-row>

    <!-- Сенсоры -->
    <v-row>
      <v-col cols="12" sm="4" v-for="(item, i) in sensorStats" :key="i">
        <v-card :color="item.color" class="pa-4 text-white" elevation="2" rounded="xl">
          <v-card-title class="d-flex justify-space-between align-center">
            {{ item.title }}
            <v-icon>{{ item.icon }}</v-icon>
          </v-card-title>
          <v-card-text class="text-h5 font-weight-bold">{{ item.value }}</v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Рекомендация -->
    <v-row>
      <v-col cols="12">
        <v-alert :type="riskColor" prominent border="start" class="mt-6">
          <div class="text-h6 mb-2">
            Bashorat: <strong>{{ prediction.recommendation || '...' }}</strong>
          </div>
          <div>Risk darajasi: <strong>{{ prediction.risk_level || '...' }}</strong></div>
          <div>Ehtimollik: {{ prediction.defect_probability ? (prediction.defect_probability * 100).toFixed(1) + '%' : '...' }}</div>
        </v-alert>
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
  name: 'OperatorView',
  data() {
    return {
      batchName: '',
      stageName: '',
      sensor: {},
      prediction: {},
      interval: null
    }
  },
  computed: {
    sensorStats() {
      return [
        {
          title: 'Harorat',
          value: this.sensor.temperature ? `${this.sensor.temperature} °C` : '...',
          icon: 'mdi-thermometer',
          color: 'deep-orange',
        },
        {
          title: 'Bosim',
          value: this.sensor.pressure ? `${this.sensor.pressure} Pa` : '...',
          icon: 'mdi-gauge',
          color: 'blue',
        },
        {
          title: 'Namlik',
          value: this.sensor.humidity ? `${this.sensor.humidity} %` : '...',
          icon: 'mdi-water-percent',
          color: 'teal',
        },
      ]
    },
    riskColor() {
      switch (this.prediction.risk_level) {
        case 'high': return 'error'
        case 'medium': return 'warning'
        case 'low': return 'success'
        default: return 'info'
      }
    }
  },
  methods: {
    async loadData() {
      try {
        const batches = await fetchBatches()
        const latestBatch = batches.at(-1)
        if (!latestBatch) return

        this.batchName = latestBatch.name || `#${latestBatch.id}`

        const stages = await fetchStagesByBatch(latestBatch.id)
        const latestStage = stages.at(-1)
        if (!latestStage) return

        this.stageName = latestStage.name || `#${latestStage.id}`

        const sensors = await fetchSensorDataByStage(latestStage.id)
        const prediction = await fetchPredictionByStage(latestStage.id)

        this.sensor = sensors.at(-1) || {}
        this.prediction = prediction?.[0] || {}
      } catch (err) {
        console.error('Operator sahifasida xatolik:', err)
      }
    }
  },
  async mounted() {
    await this.loadData()
    this.interval = setInterval(this.loadData, 5000) // 🔁 обновление каждые 5 сек
  },
  beforeUnmount() {
    clearInterval(this.interval)
  }
}
</script>
