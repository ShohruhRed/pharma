<template><canvas ref="canvas"/></template>
<script setup>
import { onMounted, ref } from 'vue'
import { Chart, registerables } from 'chart.js'
Chart.register(...registerables)

const props = defineProps({
  chartData: Object,
  chartOptions: Object
})
const canvas = ref(null)
onMounted(()=>{
  new Chart(canvas.value.getContext('2d'), {
    type: 'line',
    data: props.chartData,
    options: props.chartOptions
  })
})
</script>