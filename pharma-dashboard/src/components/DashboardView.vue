<template>
  <div>
    <h1>📈 Dashboard</h1>
    <BatchList />
    <StageTimeline />
    <SensorDataChart />
  </div>
</template>

<script>
import BatchList from "../components/BatchList.vue";
import StageTimeline from "../components/StageTimeline.vue";
import SensorDataChart from "../components/SensorDataChart.vue";

export default {
  name: "DashboardView",
  components: {
    BatchList,
    StageTimeline,
    SensorDataChart,
  },
};
</script>
