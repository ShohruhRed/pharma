<template>
  <div id="app">
    <nav>
      <router-link to="/">🏠 Dashboard</router-link>
      <router-link to="/predictions">🔍 Predictions</router-link>
    </nav>
    <main>
      <router-view />
    </main>
  </div>
</template>

<style scoped>
nav {
  background-color: #2c3e50;
  padding: 1rem;
}
nav a {
  color: #fff;
  margin-right: 1rem;
  text-decoration: none;
  font-weight: bold;
}
nav a.router-link-active {
  text-decoration: underline;
}
main {
  padding: 1.5rem;
}
</style>
