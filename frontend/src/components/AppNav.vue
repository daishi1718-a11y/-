<script setup lang="ts">
import { useRoute } from 'vue-router'
const route = useRoute()
const isActive = (p: string) => route.path === p
</script>

<template>
  <aside class="sidebar">
    <div class="brand">
      <div class="brand-mark">M</div>
      <div>
        <div class="brand-name">要員管理</div>
        <div class="brand-sub">Knowledge System</div>
      </div>
    </div>

    <nav class="nav">
      <div class="nav-group">
        <p class="group-label">OVERVIEW</p>
        <RouterLink to="/dashboard" class="nav-item" :class="{ active: isActive('/dashboard') }">
          <svg viewBox="0 0 20 20" fill="currentColor"><path d="M2 10a8 8 0 018-8v8h8a8 8 0 11-16 0z"/><path d="M12 2.252A8.014 8.014 0 0117.748 8H12V2.252z"/></svg>
          ダッシュボード
        </RouterLink>
        <RouterLink to="/search" class="nav-item" :class="{ active: isActive('/search') }">
          <svg viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd"/></svg>
          ナレッジ検索
        </RouterLink>
        <RouterLink to="/staffing" class="nav-item" :class="{ active: isActive('/staffing') }">
          <svg viewBox="0 0 20 20" fill="currentColor"><path d="M5 3a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2V5a2 2 0 00-2-2H5zM5 11a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2v-2a2 2 0 00-2-2H5zM11 5a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V5zM11 13a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"/></svg>
          稼働マトリクス
        </RouterLink>
      </div>

      <div class="nav-group">
        <p class="group-label">MASTER DATA</p>
        <RouterLink to="/employees" class="nav-item" :class="{ active: isActive('/employees') }">
          <svg viewBox="0 0 20 20" fill="currentColor"><path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z"/></svg>
          社員管理
        </RouterLink>
        <RouterLink to="/clients" class="nav-item" :class="{ active: isActive('/clients') }">
          <svg viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M4 4a2 2 0 012-2h8a2 2 0 012 2v12a1 1 0 110 2H4a1 1 0 110-2V4zm3 1h2v2H7V5zm2 4H7v2h2V9zm2-4h2v2h-2V5zm2 4h-2v2h2V9z" clip-rule="evenodd"/></svg>
          顧客管理
        </RouterLink>
        <RouterLink to="/projects" class="nav-item" :class="{ active: isActive('/projects') }">
          <svg viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M6 6V5a3 3 0 013-3h2a3 3 0 013 3v1h2a2 2 0 012 2v3.57A22.952 22.952 0 0110 13a22.95 22.95 0 01-8-1.43V8a2 2 0 012-2h2zm2-1a1 1 0 011-1h2a1 1 0 011 1v1H8V5zm1 5a1 1 0 011-1h.01a1 1 0 110 2H10a1 1 0 01-1-1z" clip-rule="evenodd"/><path d="M2 13.692V16a2 2 0 002 2h12a2 2 0 002-2v-2.308A24.974 24.974 0 0110 15c-2.796 0-5.487-.46-8-1.308z"/></svg>
          案件管理
        </RouterLink>
        <RouterLink to="/assignments" class="nav-item" :class="{ active: isActive('/assignments') }">
          <svg viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M6 2a1 1 0 00-1 1v1H4a2 2 0 00-2 2v10a2 2 0 002 2h12a2 2 0 002-2V6a2 2 0 00-2-2h-1V3a1 1 0 10-2 0v1H7V3a1 1 0 00-1-1zm0 5a1 1 0 000 2h8a1 1 0 100-2H6z" clip-rule="evenodd"/></svg>
          アサイン管理
        </RouterLink>
      </div>
    </nav>

    <div class="sidebar-footer">v1.0.0</div>
  </aside>
</template>

<style scoped>
.sidebar {
  position: fixed;
  top: 0; left: 0;
  width: var(--sidebar-w);
  height: 100vh;
  background: var(--sidebar-bg);
  border-right: 1px solid var(--sidebar-border);
  display: flex;
  flex-direction: column;
  z-index: 100;
  overflow-y: auto;
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 18px 16px;
  border-bottom: 1px solid var(--sidebar-border);
  flex-shrink: 0;
}
.brand-mark {
  width: 30px; height: 30px;
  background: var(--primary);
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  font-size: 13px; font-weight: 800; color: #fff;
  flex-shrink: 0;
}
.brand-name { font-size: 13px; font-weight: 700; color: #f1f5f9; line-height: 1.2; }
.brand-sub { font-size: 10px; color: var(--sidebar-label); letter-spacing: 0.03em; }

.nav { flex: 1; padding: 12px 8px; display: flex; flex-direction: column; gap: 16px; }
.nav-group {}
.group-label {
  font-size: 10px; font-weight: 700;
  color: var(--sidebar-label);
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: 4px 10px 6px;
}
.nav-item {
  display: flex;
  align-items: center;
  gap: 9px;
  padding: 8px 10px;
  border-radius: var(--radius);
  font-size: 13px;
  color: var(--sidebar-text);
  text-decoration: none;
  transition: background 0.1s, color 0.1s;
  border-left: 2px solid transparent;
  margin-bottom: 1px;
}
.nav-item svg { width: 15px; height: 15px; flex-shrink: 0; opacity: 0.75; }
.nav-item:hover { background: var(--sidebar-hover-bg); color: var(--sidebar-hover-text); }
.nav-item:hover svg { opacity: 1; }
.nav-item.active {
  background: var(--sidebar-active-bg);
  color: var(--sidebar-active-text);
  border-left-color: var(--sidebar-active-bar);
}
.nav-item.active svg { opacity: 1; }

.sidebar-footer {
  padding: 12px 18px;
  border-top: 1px solid var(--sidebar-border);
  font-size: 11px;
  color: var(--sidebar-label);
  flex-shrink: 0;
}
</style>
