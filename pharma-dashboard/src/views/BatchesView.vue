<template>
  <v-container fluid>
    <!-- ======== Заголовок + кнопка запуска ======== -->
    <v-card class="pa-4 mb-6" elevation="2" rounded="xl">
      <v-row align="center">
        <v-col>
          <v-card-title class="text-h6">Partiyalar ro‘yxati</v-card-title>
        </v-col>
        <v-col cols="auto">
          <v-btn color="primary" @click="onStartBatch">
            <v-icon left>mdi-play</v-icon> Yangi partiyani boshlash
          </v-btn>
        </v-col>
      </v-row>

      <!-- ======== Основная таблица ======== -->
      <v-data-table
        :headers="headers"
        :items="batches"
        class="mt-4"
        :items-per-page="20"
        density="comfortable"
      >
        <template #item.name="{ item }">
          <strong>{{ item.name || 'Partiya #' + item.id }}</strong>
        </template>

        <template #item.status="{ item }">
          <v-chip :color="statusColor(item.status)" dark>{{ item.status }}</v-chip>
        </template>

        <template #item.start_time="{ item }">
          {{ formatDate(item.start_time) }}
        </template>

        <template #item.actions="{ item }">
          <!-- Детали -->
          <v-btn icon @click="openStageDialog(item.id)">
            <v-icon>mdi-eye</v-icon>
          </v-btn>
          <!-- Остановка -->
          <v-btn
            icon
            v-if="item.status === 'active'"
            color="error"
            @click="onStopBatch(item.id)"
          >
            <v-icon>mdi-stop</v-icon>
          </v-btn>
        </template>
      </v-data-table>
    </v-card>

    <!-- ======== Модалка с этапами, графиком и прогнозами ======== -->
    <v-dialog v-model="stageDialog" max-width="900px">
      <v-card>
        <v-card-title class="text-h6">
          Partiya #{{ selectedBatchId }} — bosqichlar
        </v-card-title>
        <v-divider />

        <v-card-text>
          <v-row>
            <!-- Список этапов -->
            <v-col cols="4">
              <v-list dense>
                <v-list-item
                  v-for="stage in stages"
                  :key="stage.id"
                  :active="stage.id === selectedStageId"
                  @click="selectStage(stage.id)"
                  clickable
                >
                  <v-list-item-content>
                    <v-list-item-title>
                      {{ stage.stage_label || stage.name }}
                    </v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-list>
            </v-col>

            <!-- График + таблица предсказаний -->
            <v-col cols="8">
              <!-- График -->
              <v-card flat>
                <v-card-text>
                  <div v-if="loading">Yuklanmoqda…</div>
                  <div v-else-if="!sensorData.length">Ma’lumot topilmadi.</div>
                  <SensorDataChart
                    v-else
                    :sensorData="sensorData"
                  />
                </v-card-text>
              </v-card>

              <!-- Таблица предсказаний -->
              <v-simple-table class="predictions-table mt-4">
                <thead>
                  <tr>
                    <th>#</th>
                    <th>Sana va vaqt</th>
                    <th>Bashorat</th>
                    <th>Risk</th>
                    <th>Ehtimollik</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="(sd, idx) in sensorData"
                    :key="idx"
                    :class="[
                      'pred-row',
                      'risk-' + (predictions[idx]?.risk_level || 'none')
                    ]"
                  >
                    <td>{{ idx + 1 }}</td>
                    <td>{{ formatDate(sd.timestamp) }}</td>
                    <td>{{ predictions[idx]?.recommendation || '—' }}</td>
                    <td>{{ predictions[idx]?.risk_level || '—' }}</td>
                    <td>
                      {{
                        predictions[idx]?.defect_probability != null
                          ? (predictions[idx].defect_probability * 100).toFixed(1) + '%'
                          : '—'
                      }}
                    </td>
                  </tr>
                </tbody>
              </v-simple-table>
            </v-col>
          </v-row>
        </v-card-text>

        <v-card-actions>
          <v-spacer />
          <v-btn text @click="stageDialog = false">Yopish</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import SensorDataChart from '@/components/SensorDataChart.vue'
import {
  fetchBatches,
  fetchStagesByBatch,
  fetchSensorDataByStage,
  fetchPredictionByStage,
  startBatch,
  stopBatch
} from '@/api'

export default {
  name: 'BatchesView',
  components: { SensorDataChart },
  data() {
    return {
      headers: [
        { text: 'ID', value: 'id' },
        { text: 'Partiya', value: 'name' },
        { text: 'Holat', value: 'status' },
        { text: 'Boshlangan vaqti', value: 'start_time' },
        { text: '', value: 'actions', sortable: false }
      ],
      batches: [],

      // модалка
      stageDialog: false,
      selectedBatchId: null,
      stages: [],
      selectedStageId: null,

      // данные по этапу
      loading: false,
      sensorData: [],
      predictions: []
    }
  },
  methods: {
    formatDate(raw) {
      if (!raw) return '—'
      const [d, t] = raw.split('T')
      return `${d} ${t?.slice(0, 8) || ''}`
    },
    statusColor(status) {
      switch (status) {
        case 'active': return 'green'
        case 'stopped': return 'orange'
        case 'archived': return 'grey'
        default: return 'blue'
      }
    },
    riskColor(level) {
      switch (level) {
        case 'high': return 'error'
        case 'medium': return 'warning'
        case 'low': return 'success'
        default: return 'info'
      }
    },

    // Запуск новой партии
    async onStartBatch() {
      try {
        const newBatch = await startBatch()
        this.batches.push(newBatch)
      } catch (e) {
        console.error('Yangi partiyani boshlashda xatolik:', e)
      }
    },
    // Остановка партии
    async onStopBatch(batchId) {
      try {
        await stopBatch(batchId)
        const b = this.batches.find(x => x.id === batchId)
        if (b) b.status = 'stopped'
      } catch (e) {
        console.error('Partiyani to‘xtatishda xatolik:', e)
      }
    },

    // Открытие модалки и загрузка этапов
    async openStageDialog(batchId) {
      this.selectedBatchId = batchId
      this.stageDialog = true
      this.loading = true
      this.stages = []
      this.sensorData = []
      this.predictions = []

      try {
        this.stages = await fetchStagesByBatch(batchId)
        if (this.stages.length) {
          await this.selectStage(this.stages[0].id)
        }
      } catch (e) {
        console.error('Etaplarni yuklashda xatolik:', e)
      } finally {
        this.loading = false
      }
    },
    // Выбор этапа внутри модалки
    async selectStage(stageId) {
      this.selectedStageId = stageId
      this.loading = true
      try {
        this.sensorData = await fetchSensorDataByStage(stageId)
        this.predictions = await fetchPredictionByStage(stageId)
      } catch (e) {
        console.error('Ma’lumotlarni yuklashda xatolik:', e)
        this.sensorData = []
        this.predictions = []
      } finally {
        this.loading = false
      }
    }
  },
  async mounted() {
    try {
      this.batches = await fetchBatches()
    } catch (e) {
      console.error('Partiyalarni yuklashda xatolik:', e)
    }
  }
}
</script>

<style scoped>
/* Основная таблица */
.v-data-table thead th {
  background: #f5f5f5;
  color: #333;
  font-weight: 600;
  text-transform: uppercase;
  padding: 12px;
}
.v-data-table tbody td {
  padding: 12px;
  font-size: 14px;
}

/* Таблица предсказаний */
.predictions-table {
  width: 100%;
}
.predictions-table thead th,
.predictions-table tbody td {
  padding: 10px 12px;
  border-bottom: 1px solid #eee;
  font-size: 14px;
  text-align: left;
}
.pred-row.risk-high   { background-color: #fee2e2; }
.pred-row.risk-medium { background-color: #fef3c7; }
.pred-row.risk-low    { background-color: #d1fae5; }
</style>
