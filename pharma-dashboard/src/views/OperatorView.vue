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

    <!-- Сенсорлар -->
    <v-row>
      <v-col cols="12" sm="4" v-for="(item, i) in sensorStats" :key="i">
      <v-card
          :color="item.color"
          :class="['pa-4 text-white position-relative', highlighted ? 'pulse-card' : '']"
          elevation="2"
          rounded="xl"
        >
          <!-- Иконка риска -->
          <v-icon
            :color="riskColorClass"
            size="20"
            class="position-absolute top-0 right-0 mt-2 mr-2"
            style="background: white; border-radius: 50%; padding: 2px;"
          >
            {{ riskIcon }}
          </v-icon>

          <!-- Основное содержимое -->
          <v-card-title class="d-flex justify-space-between align-center">
            {{ item.title }}
            <v-icon>{{ item.icon }}</v-icon>
          </v-card-title>
          <v-card-text class="text-h5 font-weight-bold">{{ item.value }}</v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Rekomendatsiya -->
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
  fetchCurrentStageData,
  fetchPredictionByStage
} from '@/api'

export default {
  name: 'OperatorView',
  data() {
    return {
      batchName: '',
      stageName: '',
      sensor: {},
      prevSensor: {},
      highlighted: false,
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
    },
    riskIcon() {
      switch (this.prediction.risk_level) {
        case 'high': return 'mdi-alert-circle'
        case 'medium': return 'mdi-alert'
        case 'low': return 'mdi-check-circle'
        default: return 'mdi-help-circle'
      }
    },
    riskColorClass() {
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
        const data = await fetchCurrentStageData()

        this.batchName = data.batch.name || `#${data.batch.id}`
        this.stageName = data.stage.stage_label || `#${data.stage.id}`

        const newSensor = data.sensor_data

        // Сравнение с предыдущими значениями
        const changed = (
          this.prevSensor.temperature !== newSensor.temperature ||
          this.prevSensor.pressure !== newSensor.pressure ||
          this.prevSensor.humidity !== newSensor.humidity
        )

        this.sensor = newSensor

        if (changed) {
          this.highlighted = true
          setTimeout(() => { this.highlighted = false }, 1000)
        }

        this.prevSensor = { ...newSensor }

        const prediction = await fetchPredictionByStage(data.stage.id)
        this.prediction = prediction?.[0] || {}

      } catch (err) {
        console.error('Operator sahifasida xatolik:', err)
      }
    }
  },
  async mounted() {
    await this.loadData()
    this.interval = setInterval(this.loadData, 5000)
  },
  beforeUnmount() {
    clearInterval(this.interval)
  }
}
</script>

<style scoped>
.pulse-card {
  animation: pulse 0.6s ease-in-out;
}

@keyframes pulse {
  0% {
    transform: scale(1);
    box-shadow: 0 0 0px rgba(255, 255, 255, 0.5);
  }
  50% {
    transform: scale(1.03);
    box-shadow: 0 0 20px rgba(255, 255, 255, 0.9);
  }
  100% {
    transform: scale(1);
    box-shadow: 0 0 0px rgba(255, 255, 255, 0.5);
  }
}
</style>

