<template>
  <div class="skeleton-card"></div>
</template>
<script>
export default { name: 'SkeletonCard' }
</script>
<style lang="scss" scoped>

.skeleton-card {
  height: 100px;
  border-radius: $radius;
  background: $color-border;
  animation: pulse 1.2s infinite ease-in-out;
  margin-bottom: $spacing-md;
}

@keyframes pulse {
  0%   { opacity: 1; }
  50%  { opacity: 0.4; }
  100% { opacity: 1; }
}
</style>
