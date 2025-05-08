<template>
  <div>
    <v-skeleton-loader
      v-if="!sensorData || sensorData.length === 0"
      type="image"
      class="my-6"
    />
    <line-chart
      v-else
      :data="chartData"
      :options="chartOptions"
    />
  </div>
</template>

<script>
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement
} from 'chart.js'

import { Line } from 'vue-chartjs'

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  CategoryScale,
  LinearScale,
  PointElement
)

export default {
  name: 'SensorDataChart',
  components: {
    LineChart: Line
  },
  props: {
    sensorData: {
      type: Array,
      required: true
    }
  },
  computed: {
    chartData() {
      const labels = this.sensorData.map((_, i) => `T${i + 1}`)
      return {
        labels,
        datasets: [
          {
            label: 'Harorat (°C)',
            data: this.sensorData.map(d => d.temperature),
            borderColor: 'rgba(255, 99, 132, 1)',
            backgroundColor: 'rgba(255, 99, 132, 0.1)',
            fill: true,
            tension: 0.4
          },
          {
            label: 'Bosim (Pa)',
            data: this.sensorData.map(d => d.pressure),
            borderColor: 'rgba(54, 162, 235, 1)',
            backgroundColor: 'rgba(54, 162, 235, 0.1)',
            fill: true,
            tension: 0.4
          },
          {
            label: 'Namlik (%)',
            data: this.sensorData.map(d => d.humidity),
            borderColor: 'rgba(75, 192, 192, 1)',
            backgroundColor: 'rgba(75, 192, 192, 0.1)',
            fill: true,
            tension: 0.4
          }
        ]
      }
    },
    chartOptions() {
      return {
        responsive: true,
        plugins: {
          legend: { position: 'top' },
          title: {
            display: true,
            text: 'Sensor o‘lchovlari'
          }
        }
      }
    }
  }
}
</script>
