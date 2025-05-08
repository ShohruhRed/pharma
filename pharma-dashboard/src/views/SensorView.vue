<template>
  <v-container>
    <!-- Карточки -->
    <v-row>
      <v-col cols="12" md="4" v-for="(item, i) in latestStats" :key="i">
        <v-card :color="item.color" class="pa-4 text-white" rounded="xl" elevation="3">
          <v-card-title class="d-flex justify-space-between align-center">
            {{ item.title }}
            <v-icon>{{ item.icon }}</v-icon>
          </v-card-title>
          <v-card-text class="text-h5 font-weight-bold">
            {{ item.value }}
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- График -->
    <v-row>
      <v-col cols="12">
        <v-card elevation="2" class="pa-4" rounded="xl">
          <v-card-title class="text-h6">
            <v-icon class="me-2">mdi-chart-line</v-icon>
            Sensor ma’lumotlari
          </v-card-title>
          <v-card-text>
            <SensorDataChart :sensorData="sensorData" />
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Таблица -->
    <v-row>
      <v-col cols="12">
        <v-card class="pa-4 mt-6" elevation="1" rounded="xl">
          <v-card-title class="text-h6">Sensor o‘lchovlar jadvali</v-card-title>
          <v-data-table
            :headers="headers"
            :items="sensorData"
            class="elevation-0 mt-3"
            dense
            disable-pagination
            hide-default-footer
          />
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
// ✅ IMPORT НА САМОМ ВЕРХУ
import SensorDataChart from '@/components/SensorDataChart.vue'
import {
  fetchBatches,
  fetchStagesByBatch,
  fetchSensorDataByStage,
} from '@/api'

export default {
  name: 'SensorView',
  components: {
    SensorDataChart,
  },
  data() {
    return {
      sensorData: [],
    }
  },
  computed: {
    latestStats() {
      const latest = this.sensorData.at(-1) || {}
      return [
        {
          title: 'Oxirgi harorat',
          value: latest.temperature ? `${latest.temperature} °C` : '...',
          icon: 'mdi-thermometer',
          color: 'deep-orange',
        },
        {
          title: 'Oxirgi bosim',
          value: latest.pressure ? `${latest.pressure} Pa` : '...',
          icon: 'mdi-gauge',
          color: 'blue',
        },
        {
          title: 'Oxirgi namlik',
          value: latest.humidity ? `${latest.humidity} %` : '...',
          icon: 'mdi-water-percent',
          color: 'teal',
        },
      ]
    },
    headers() {
      return [
        { text: '№', value: 'index' },
        { text: 'Harorat (°C)', value: 'temperature' },
        { text: 'Bosim (Pa)', value: 'pressure' },
        { text: 'Namlik (%)', value: 'humidity' },
      ]
    },
  },
  async mounted() {
    try {
      const batches = await fetchBatches()
      const latestBatch = batches.at(-1)
      if (!latestBatch) return

      const stages = await fetchStagesByBatch(latestBatch.id)
      const latestStage = stages.at(-1)
      if (!latestStage) return

      const data = await fetchSensorDataByStage(latestStage.id)

      this.sensorData = data.map((item, i) => ({
        ...item,
        index: i + 1,
      }))
    } catch (err) {
      console.error('Xatolik sensor sahifasida:', err)
    }
  },
}
</script>
