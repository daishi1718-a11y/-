<script setup lang="ts">
import AppNav from '@/components/AppNav.vue'
</script>

<template>
  <div class="shell">
    <AppNav />
    <div class="main">
      <RouterView />
    </div>
  </div>
</template>

<style>
:root {
  --sidebar-w: 220px;
  --sidebar-bg: #0f172a;
  --sidebar-border: #1e293b;
  --sidebar-label: #475569;
  --sidebar-text: #94a3b8;
  --sidebar-hover-bg: rgba(255,255,255,0.05);
  --sidebar-hover-text: #e2e8f0;
  --sidebar-active-bg: rgba(59,130,246,0.12);
  --sidebar-active-text: #60a5fa;
  --sidebar-active-bar: #3b82f6;

  --bg: #f1f5f9;
  --surface: #ffffff;
  --surface-sub: #f8fafc;
  --border: #e2e8f0;
  --border-strong: #cbd5e1;

  --text: #0f172a;
  --text-2: #475569;
  --text-3: #94a3b8;

  --primary: #2563eb;
  --primary-dark: #1d4ed8;
  --primary-bg: #eff6ff;

  --green: #16a34a;
  --green-bg: #f0fdf4;
  --green-text: #166534;
  --amber: #d97706;
  --amber-bg: #fffbeb;
  --amber-text: #78350f;
  --red: #dc2626;
  --red-bg: #fef2f2;
  --red-text: #991b1b;
  --slate-bg: #f1f5f9;
  --slate-text: #475569;

  --radius: 6px;
  --radius-lg: 10px;
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
  --shadow: 0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.04);
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'Hiragino Sans', 'Noto Sans JP', 'Yu Gothic UI', system-ui, sans-serif;
  background: var(--bg);
  color: var(--text);
  font-size: 14px;
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
}

.shell { display: flex; min-height: 100vh; }
.main { flex: 1; margin-left: var(--sidebar-w); min-height: 100vh; overflow-x: auto; }

/* ── Shared layout ──────────────────────────────── */
.page { padding: 32px; max-width: 1400px; }

.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 24px;
  gap: 16px;
}
.page-title { font-size: 20px; font-weight: 700; color: var(--text); line-height: 1.25; }
.page-desc { font-size: 13px; color: var(--text-3); margin-top: 3px; }
.count-badge {
  display: inline-flex;
  align-items: center;
  padding: 1px 8px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  background: var(--border);
  color: var(--text-2);
  margin-left: 8px;
  vertical-align: middle;
}

/* ── Card ───────────────────────────────────────── */
.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
}
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 20px;
  border-bottom: 1px solid var(--border);
}
.card-title { font-size: 14px; font-weight: 600; color: var(--text); }
.card-body { padding: 20px; }

/* ── Buttons ────────────────────────────────────── */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 7px 14px;
  font-size: 13px;
  font-weight: 500;
  border-radius: var(--radius);
  cursor: pointer;
  transition: background 0.12s, border-color 0.12s, color 0.12s;
  border: 1px solid transparent;
  line-height: 1.4;
  white-space: nowrap;
  font-family: inherit;
}
.btn:disabled { opacity: 0.45; cursor: not-allowed; }
.btn svg { width: 14px; height: 14px; flex-shrink: 0; }

.btn-primary  { background: var(--primary); color: #fff; border-color: var(--primary); }
.btn-primary:hover:not(:disabled)  { background: var(--primary-dark); border-color: var(--primary-dark); }

.btn-secondary { background: var(--surface); color: var(--text-2); border-color: var(--border-strong); }
.btn-secondary:hover:not(:disabled) { background: var(--surface-sub); }

.btn-danger { background: var(--surface); color: var(--red); border-color: var(--red); }
.btn-danger:hover:not(:disabled) { background: var(--red-bg); }

.btn-ghost { background: transparent; color: var(--text-2); border-color: transparent; }
.btn-ghost:hover:not(:disabled) { background: var(--border); }

.btn-sm { padding: 5px 10px; font-size: 12px; }

/* ── Form ───────────────────────────────────────── */
.form-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; }
.form-grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 14px; }
.span2 { grid-column: span 2; }
.span3 { grid-column: 1 / -1; }

.field {
  display: flex;
  flex-direction: column;
  gap: 5px;
  font-size: 13px;
  font-weight: 500;
  color: var(--text-2);
}
.field input,
.field select,
.field textarea {
  padding: 7px 10px;
  border: 1px solid var(--border-strong);
  border-radius: var(--radius);
  font-size: 13px;
  color: var(--text);
  background: var(--surface);
  transition: border-color 0.12s, box-shadow 0.12s;
  width: 100%;
  font-family: inherit;
}
.field input:focus,
.field select:focus,
.field textarea:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(37,99,235,0.1);
}
.field input::placeholder { color: var(--text-3); }
.req { color: var(--red); font-size: 10px; margin-left: 2px; }

.form-section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}
.form-section-title { font-size: 14px; font-weight: 600; }
.form-actions { display: flex; gap: 8px; margin-top: 20px; align-items: center; }
.form-actions-sep { flex: 1; }

/* ── Table ──────────────────────────────────────── */
.data-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.data-table th {
  padding: 10px 16px;
  background: var(--surface-sub);
  border-bottom: 1px solid var(--border);
  font-weight: 600;
  color: var(--text-2);
  text-align: left;
  white-space: nowrap;
  font-size: 11px;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}
.data-table td {
  padding: 11px 16px;
  border-bottom: 1px solid var(--border);
  color: var(--text);
  vertical-align: middle;
}
.data-table tbody tr:last-child td { border-bottom: none; }
.data-table tbody tr.row-clickable { cursor: pointer; transition: background 0.1s; }
.data-table tbody tr.row-clickable:hover { background: #f8fafc; }
.data-table tbody tr.row-selected { background: var(--primary-bg) !important; }
.data-table tbody tr.row-selected td { border-bottom-color: #dbeafe; }
.data-table tbody tr.row-detail td { padding: 0; background: #f8fafc; border-bottom: 2px solid var(--border); }
.data-table td.nowrap { white-space: nowrap; }
.data-table td.text-right { text-align: right; }
.data-table td.text-mono { font-family: 'JetBrains Mono', 'Courier New', monospace; font-size: 12px; }

/* ── Badges ─────────────────────────────────────── */
.badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 2px 8px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.02em;
  white-space: nowrap;
}
.badge-active  { background: var(--green-bg);  color: var(--green-text); }
.badge-pending { background: var(--amber-bg);  color: var(--amber-text); }
.badge-done    { background: var(--slate-bg);  color: var(--slate-text); }
.badge-info    { background: var(--primary-bg); color: var(--primary-dark); }

/* ── Misc ───────────────────────────────────────── */
.empty-state {
  padding: 48px 24px;
  text-align: center;
  color: var(--text-3);
  font-size: 13px;
}
.error-banner {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 12px 16px;
  background: var(--red-bg);
  border: 1px solid #fecaca;
  border-radius: var(--radius);
  color: var(--red-text);
  font-size: 13px;
  margin-bottom: 20px;
}
.inline-label {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  cursor: pointer;
  font-weight: 400;
}
</style>
