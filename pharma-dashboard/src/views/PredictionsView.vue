<!-- src/views/PredictionsView.vue -->
<template>
  <div>
    <h1>Прогнозы</h1>
    <ul>
      <li v-for="p in predictions" :key="p.id">
        {{ p.timestamp }} — {{ p.defect_probability }} ({{ p.risk_level }})
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { fetchAllPredictions } from '@/api'   // создайте эту функцию в src/api/index.js

const predictions = ref([])

onMounted(async () => {
  const res = await fetchAllPredictions()
  predictions.value = res.data
})
</script>


<style lang="scss" scoped>

.predictions-view {
  @include card;
  padding: $spacing-md;
  overflow-x: auto;

  h2 {
    margin-bottom: $spacing-md;
  }

  table {
    width: 100%;
    border-collapse: collapse;

    thead {
      background: $color-primary;
      th {
        color: #fff;
        padding: $spacing-sm;
        text-align: left;
      }
    }

    tbody {
      tr + tr {
        border-top: 1px solid $color-border;
      }

      td {
        padding: $spacing-sm;
      }
    }
  }

  .no-data {
    color: $text-muted;
    text-align: center;
    padding: $spacing-md;
  }
}
</style>
