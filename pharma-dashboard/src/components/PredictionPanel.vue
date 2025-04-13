<template>
  <div>
    <h1>📍 Predictions</h1>
    <PredictionPanel />
  </div>
</template>

<script>
import PredictionPanel from "../components/PredictionPanel.vue";

export default {
  name: "PredictionsView",
  components: {
    PredictionPanel,
  },
};
</script>
