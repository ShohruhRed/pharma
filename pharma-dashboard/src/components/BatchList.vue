<template>
  <div class="batch-list">
    <h2>📦 Партии</h2>
    <ul>
      <li v-for="b in batches" :key="b.id" @click="$emit('select', b.id)">
        #{{ b.id }} — {{ b.status }}
      </li>
    </ul>
  </div>
</template>
<script>
export default {
  props: { batches: Array }
}
</script>
<style lang="scss" scoped>

.batch-list {
  @include card;
  padding: $spacing-md;
  ul { list-style: none; }
  li {
    padding: $spacing-sm;
    cursor: pointer;
    &:hover { background: $color-bg; }
  }
}
</style>
