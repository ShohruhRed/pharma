<template>
  <v-container>
    <v-card elevation="2" class="pa-4" rounded="xl">
      <v-card-title class="text-h6">Partiyalar ro‘yxati</v-card-title>

      <v-data-table
        :headers="headers"
        :items="batches"
        class="mt-4"
        density="comfortable"
        :items-per-page="100"
      >
        <!-- Nomi -->
        <template v-slot:item.name="{ item }">
          {{ item.name || 'Partiya #' + item.id }}
        </template>

        <!-- Holat -->
        <template v-slot:item.status="{ item }">
          <v-chip :color="statusColor(item.status)" dark>{{ item.status }}</v-chip>
        </template>

        <!-- Sana -->
        <template v-slot:item.created_at="{ item }">
          {{ formatDate(item.created_at) }}
        </template>
      </v-data-table>
    </v-card>
  </v-container>
</template>

<script>
import { fetchBatches } from '@/api'

export default {
  name: 'BatchesView',
  data() {
    return {
      headers: [
        { text: 'ID', value: 'id' },
        { text: 'Partiya', value: 'name' },
        { text: 'Holat', value: 'status' },
        { text: 'Boshlangan vaqti', value: 'created_at' }
      ],
      batches: []
    }
  },
  methods: {
    formatDate(raw) {
      if (!raw || typeof raw !== 'string') return '—'
      const [date, time] = raw.split(' ')
      const shortTime = time?.slice(0, 8) || ''
      return `${date} ${shortTime}`
    },
    statusColor(status) {
      switch (status) {
        case 'active': return 'green'
        case 'stopped': return 'orange'
        case 'archived': return 'grey'
        default: return 'blue'
      }
    }
  },
  async mounted() {
    this.batches = await fetchBatches()
  }
}
</script>

<style scoped>
/* 🎯 Стиль заголовков таблицы */
.v-data-table thead {
  background-color: #f5f5f5;
}
.v-data-table thead th {
  color: #000;
  font-weight: bold;
  font-size: 14px;
  text-transform: uppercase;
}
</style>
