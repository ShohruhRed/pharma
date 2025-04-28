<template>
  <div class="chart-container">
    <canvas ref="canvas"></canvas>
  </div>
</template>

<script>
import { onMounted, ref, watch } from 'vue'
import { Chart, registerables } from 'chart.js'

Chart.register(...registerables)

export default {
  name: 'SensorDataChart',
  props: {
    data: {
      type: Array,
      default: () => []
    }
  },
  setup(props) {
    const canvas = ref(null)
    let chart = null

    // Функция для (пере)отрисовки графика
    const renderChart = () => {
      if (!canvas.value) return
      const ctx = canvas.value.getContext('2d')

      // разрушим предыдущий, если есть
      if (chart) chart.destroy()

      // подготовим метки и серии
      const labels = props.data.map(d =>
        new Date(d.timestamp).toLocaleTimeString()
      )
      const temps = props.data.map(d => d.temperature)
      const pressures = props.data.map(d => d.pressure)
      const hums = props.data.map(d => d.humidity)

      chart = new Chart(ctx, {
        type: 'line',
        data: {
          labels,
          datasets: [
            {
              label: 'Temperature (°C)',
              data: temps,
              borderWidth: 2,
              tension: 0.2,
              borderColor: '#ff6384',
              fill: false,
            },
            {
              label: 'Pressure (bar)',
              data: pressures,
              borderWidth: 2,
              tension: 0.2,
              borderColor: '#36a2eb',
              fill: false,
            },
            {
              label: 'Humidity (%)',
              data: hums,
              borderWidth: 2,
              tension: 0.2,
              borderColor: '#ffcd56',
              fill: false,
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          interaction: { mode: 'index', intersect: false },
          plugins: {
            legend: { position: 'top' },
            tooltip: { enabled: true },
          },
          scales: {
            x: {
              display: true,
              title: { display: true, text: 'Time' }
            },
            y: {
              display: true,
              title: { display: true, text: 'Value' }
            }
          }
        }
      })
    }

    onMounted(renderChart)
    watch(() => props.data, renderChart, { deep: true })

    return { canvas }
  }
}
</script>

<style scoped>
.chart-container {
  position: relative;
  width: 100%;
  height: 300px;
  background: var(--color-surface);
  border-radius: var(--radius-md);
  padding: var(--spacing-sm);
  box-shadow: var(--shadow-sm);
}
</style>
