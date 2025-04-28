<template>
  <div class="prediction-panel" :class="risk">
    <div class="icon">{{ icon }}</div>
    <div class="details">
      <div class="probability">{{ (prediction.defect_probability * 100).toFixed(1) }}%</div>
      <div class="risk-level">{{ riskLabel }}</div>
      <div class="recommendation">{{ prediction.recommendation }}</div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PredictionPanel',
  props: {
    prediction: {
      type: Object,
      required: true
    }
  },
  computed: {
    risk() {
      return this.prediction.risk_level // "low", "medium" или "high"
    },
    icon() {
      return { low: '🟢', medium: '🟡', high: '🔴' }[this.risk]
    },
    riskLabel() {
      return { low: 'Низкий риск', medium: 'Средний риск', high: 'Высокий риск' }[this.risk]
    }
  }
}
</script>

<style scoped lang="scss">
.prediction-panel {
  display: flex;
  align-items: center;
  padding: $spacing-sm;
  border-radius: $radius-md;
  box-shadow: $shadow-sm;
  &.low    { background: #e8f5e9; }
  &.medium { background: #fff8e1; }
  &.high   { background: #ffebee; }

  .icon {
    font-size: 2.5rem;
    margin-right: $spacing-md;
  }
  .details {
    .probability {
      font-size: 1.75rem;
      font-weight: bold;
      margin-bottom: $spacing-xs;
    }
    .risk-level {
      font-size: 1.1rem;
      margin-bottom: $spacing-xs;
    }
    .recommendation {
      font-size: 0.9rem;
      color: $color-on-surface-variant;
    }
  }
}
</style>
