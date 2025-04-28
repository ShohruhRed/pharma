<template>
  <div class="stage-timeline">
    <h3>⏱ Этапы</h3>
    <ul>
      <li v-for="s in stages" :key="s.id" @click="$emit('select', s.id)">
        {{ s.name }}
      </li>
    </ul>
  </div>
</template>
<script>
export default {
  props: { stages: Array }
}
</script>
<style lang="scss" scoped>

.stage-timeline {
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
