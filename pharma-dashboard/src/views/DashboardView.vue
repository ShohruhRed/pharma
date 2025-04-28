<template>
  <div class="dashboard-grid">
    <aside class="sidebar">
      <h3><i class="fa fa-box"></i> Партии</h3>
      <BatchList :batches="batchList" @select="onBatchSelect" />

      <h3><i class="fa fa-clock"></i> Этапы</h3>
      <StageTimeline :stages="stageList" @select="onStageSelect" />
    </aside>

    <main class="main-panel">
      <section class="chart-section">
        <h3><i class="fa fa-chart-line"></i> Сенсорные данные</h3>
        <SensorDataChart :data="sensorData" />
      </section>

      <section class="prediction-section" v-if="prediction">
        <h3><i class="fa fa-bell"></i> Прогноз</h3>
        <PredictionPanel :prediction="prediction" />
      </section>
    </main>
  </div>
</template>

<script>
import BatchList from '@/components/BatchList.vue'
import StageTimeline from '@/components/StageTimeline.vue'
import SensorDataChart from '@/components/SensorDataChart.vue'
import PredictionPanel from '@/components/PredictionPanel.vue'
import { fetchBatches, fetchStagesByBatch, fetchSensorDataByStage, fetchPredictionByStage } from '@/api'

export default {
  components: { BatchList, StageTimeline, SensorDataChart, PredictionPanel },
  data() {
    return {
      batchList: [],
      stageList: [],
      sensorData: [],
      prediction: null
    }
  },
  methods: {
    async onBatchSelect(id) {
      this.stageList = await fetchStagesByBatch(id)
      this.sensorData = []
      this.prediction = null
    },
    async onStageSelect(id) {
      this.sensorData = await fetchSensorDataByStage(id)
      this.prediction = await fetchPredictionByStage(id)
    }
  },
  async mounted() {
    this.batchList = await fetchBatches()
  }
}
</script>

<style scoped>
.dashboard-grid {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: var(--spacing-md);
  padding: var(--spacing-md);
}

.sidebar {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  padding: var(--spacing-md);
  box-shadow: var(--shadow-md);
  h3 {
    font-size: 1rem;
    margin-top: var(--spacing-md);
    margin-bottom: var(--spacing-xs);
    display: flex;
    align-items: center;
    i { margin-right: var(--spacing-xs); }
  }
}

.main-panel {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.chart-section, .prediction-section {
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  padding: var(--spacing-md);
  box-shadow: var(--shadow-md);
  h3 {
    font-size: 1rem;
    margin-bottom: var(--spacing-sm);
    display: flex;
    align-items: center;
    i { margin-right: var(--spacing-xs); }
  }
}
</style>
