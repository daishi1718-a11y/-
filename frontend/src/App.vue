<script setup lang="ts">
import AppNav from '@/components/AppNav.vue'
</script>

<template>
  <AppNav />
  <RouterView />
</template>

<style>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}
body {
  font-family: system-ui, sans-serif;
  background: #f8fafc;
  color: #1e293b;
}
</style>
