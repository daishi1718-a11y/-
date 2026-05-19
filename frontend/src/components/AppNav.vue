<script setup lang="ts"></script>

<template>
  <nav class="nav">
    <span class="nav-title">案件・要員管理</span>
    <RouterLink to="/search" class="highlight">🔍 ナレッジ検索</RouterLink>
    <span class="sep">|</span>
    <RouterLink to="/staffing">稼働マトリクス</RouterLink>
    <RouterLink to="/employees">社員管理</RouterLink>
    <RouterLink to="/projects">案件管理</RouterLink>
    <RouterLink to="/clients">顧客管理</RouterLink>
    <RouterLink to="/assignments">アサイン管理</RouterLink>
  </nav>
</template>

<style scoped>
.nav {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 0.75rem 1.5rem;
  background: #1e293b;
  color: #f8fafc;
}
.nav-title {
  font-weight: bold;
  margin-right: 1rem;
}
.nav a {
  color: #94a3b8;
  text-decoration: none;
  font-size: 0.9rem;
}
.nav a:hover,
.nav a.router-link-active {
  color: #f8fafc;
}
.nav a.highlight {
  color: #7dd3fc;
}
.nav a.highlight:hover,
.nav a.highlight.router-link-active {
  color: #fff;
}
.sep {
  color: #334155;
  font-size: 0.8rem;
}
</style>
