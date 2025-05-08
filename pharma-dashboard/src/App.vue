<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-app-bar-title>AI Dasturxona</v-app-bar-title>
    </v-app-bar>

    <v-navigation-drawer app permanent>
      <v-list nav>
        <v-list-item to="/dashboard" title="Dashboard" prepend-icon="mdi-view-dashboard" />
        <v-list-item to="/batches" title="Partiyalar" prepend-icon="mdi-package-variant-closed" />
        <v-list-item to="/sensors" title="Sensorlar" prepend-icon="mdi-chart-line" />
        <v-list-item to="/predictions" title="AI Bashoratlar" prepend-icon="mdi-brain" />
        <v-list-item to="/operator" title="Operator" prepend-icon="mdi-monitor" />
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>
