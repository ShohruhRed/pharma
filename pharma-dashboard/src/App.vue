<template>
  <div class="app">
    <header class="app__header">
      <h1 class="app__logo">🧪 PharmaDash</h1>
      <nav class="app__nav">
        <router-link to="/dashboard" active-class="active">Dashboard</router-link>
        <router-link to="/predictions" active-class="active">History</router-link>
      </nav>
    </header>
    <main class="app__content">
      <router-view />
    </main>
    <footer class="app__footer">
      © 2025 PharmaDash Inc.
    </footer>
  </div>
</template>

<script>
export default { name: 'App' }
</script>

<style lang="scss" scoped>

.app {
  display: grid;
  grid-template-rows: auto 1fr auto;
  height: 100vh;
  background: $color-bg;
}
.app__header {
  @include card;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: $spacing-md $spacing-lg;
  .app__logo { font-size: 1.5rem; }
  .app__nav a {
    margin-left: $spacing-md;
    color: $text-dark;
    font-weight: 500;
    padding: $spacing-sm $spacing-md;
    border-radius: $radius / 2;
    transition: background 0.2s;
    &.active { background: $color-primary; color: #fff; }
    &:hover { background: lighten($color-primary, 20%); color: #fff; }
  }
}
.app__content {
  padding: $spacing-lg;
  overflow-y: auto;
}
.app__footer {
  @include card;
  text-align: center;
  padding: $spacing-sm;
  font-size: 0.85rem;
  color: $text-muted;
}
</style>
