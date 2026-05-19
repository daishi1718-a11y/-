<script setup lang="ts">
import { extractError } from '@/api/client'
import { ref, onMounted } from 'vue'
import { getStaffingMatrix } from '@/api/staffing'
import type { StaffingMatrix, StaffingCell } from '@/types/staffing'

function currentYearMonth(): string {
  const d = new Date()
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`
}

function addMonths(ym: string, n: number): string {
  const parts = ym.split('-')
  const y = Number(parts[0])
  const m = Number(parts[1])
  const date = new Date(y, m - 1 + n, 1)
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`
}

function monthLabel(ym: string): string {
  const m = parseInt(ym.slice(-2), 10)
  return `${m}月`
}

const fromMonth = ref(currentYearMonth())
const toMonth = ref(addMonths(currentYearMonth(), 5))
const matrix = ref<StaffingMatrix | null>(null)
const error = ref('')
const loading = ref(false)

async function load() {
  if (fromMonth.value > toMonth.value) {
    error.value = '表示開始月は表示終了月以前を指定してください'
    return
  }
  loading.value = true
  error.value = ''
  try {
    matrix.value = await getStaffingMatrix(fromMonth.value, toMonth.value)
  } catch (e) {
    error.value = extractError(e)
  } finally {
    loading.value = false
  }
}

function cellClass(cell: StaffingCell | undefined): string {
  if (!cell || cell.status === '空き') return 'mc-empty'
  if (cell.count > 1) return 'mc-multi'
  if (cell.status === '内諾') return 'mc-naidaku'
  return 'mc-busy'
}

function cellLabel(cell: StaffingCell | undefined): string {
  if (!cell || cell.status === '空き') return ''
  if (cell.count > 1) return `×${cell.count}`
  return '●'
}

onMounted(load)
</script>

<template>
  <div class="page">
    <div class="page-header">
      <div>
        <div class="page-title">稼働マトリクス</div>
        <div class="page-desc">社員ごとの月別アサイン状況</div>
      </div>
      <div class="controls">
        <div class="field" style="flex-direction:row;align-items:center;gap:8px;margin:0">
          <span style="font-size:12px;color:var(--text-3);white-space:nowrap">開始月</span>
          <input type="month" v-model="fromMonth" style="padding:6px 10px;border:1px solid var(--border-strong);border-radius:var(--radius);font-size:13px;font-family:inherit" />
        </div>
        <span style="color:var(--text-3);font-size:13px">〜</span>
        <div class="field" style="flex-direction:row;align-items:center;gap:8px;margin:0">
          <span style="font-size:12px;color:var(--text-3);white-space:nowrap">終了月</span>
          <input type="month" v-model="toMonth" style="padding:6px 10px;border:1px solid var(--border-strong);border-radius:var(--radius);font-size:13px;font-family:inherit" />
        </div>
        <button class="btn btn-primary" @click="load" :disabled="loading">
          <svg viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clip-rule="evenodd"/></svg>
          {{ loading ? '読み込み中...' : '表示' }}
        </button>
      </div>
    </div>

    <div v-if="error" class="error-banner">
      <svg viewBox="0 0 20 20" fill="currentColor" style="width:16px;height:16px;flex-shrink:0;margin-top:1px"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/></svg>
      {{ error }}
    </div>

    <div v-if="matrix" class="card" style="overflow:hidden">
      <div style="overflow-x:auto">
        <table class="matrix-table">
          <thead>
            <tr>
              <th class="name-col">社員名</th>
              <th v-for="m in matrix.months" :key="m" class="month-col">{{ monthLabel(m) }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="row in matrix.rows" :key="row.employee_id">
              <td class="name-col">{{ row.employee_name }}</td>
              <td
                v-for="m in matrix.months"
                :key="m"
                :class="['month-cell', cellClass(row.cells[m])]"
                :title="row.cells[m]?.project_name ?? ''"
              >
                {{ cellLabel(row.cells[m]) }}
              </td>
            </tr>
            <tr v-if="!matrix.rows.length">
              <td :colspan="(matrix.months.length || 0) + 1" class="empty-state">データがありません</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="legend-bar">
        <span class="legend-item"><span class="lc lc-busy"></span>契約期間中</span>
        <span class="legend-item"><span class="lc lc-naidaku"></span>内諾</span>
        <span class="legend-item"><span class="lc lc-multi"></span>複数</span>
        <span class="legend-item"><span class="lc lc-empty"></span>空き</span>
      </div>
    </div>

    <div v-else-if="!loading && !error" class="card">
      <div class="empty-state">「表示」ボタンを押してデータを読み込んでください</div>
    </div>
  </div>
</template>

<style scoped>
.controls {
  display: flex;
  align-items: center;
  gap: 10px;
}

.matrix-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}
.matrix-table th {
  padding: 10px 12px;
  background: var(--surface-sub);
  border-bottom: 1px solid var(--border);
  font-weight: 600;
  color: var(--text-2);
  font-size: 11px;
  letter-spacing: 0.04em;
  white-space: nowrap;
}
.matrix-table td {
  padding: 9px 12px;
  border-bottom: 1px solid var(--border);
  vertical-align: middle;
}
.matrix-table tbody tr:last-child td { border-bottom: none; }

.name-col {
  text-align: left;
  min-width: 140px;
  font-weight: 500;
}
.month-col {
  text-align: center;
  min-width: 80px;
}
.month-cell {
  text-align: center;
  font-size: 11px;
  font-weight: 600;
  min-width: 80px;
}

.mc-busy    { background: #dcfce7; color: #166534; }
.mc-naidaku { background: #fffbeb; color: #78350f; }
.mc-multi   { background: #fef9c3; color: #713f12; }
.mc-empty   { background: #fee2e2; color: #991b1b; }

.legend-bar {
  display: flex;
  gap: 20px;
  padding: 12px 16px;
  border-top: 1px solid var(--border);
  font-size: 12px;
  color: var(--text-2);
  background: var(--surface-sub);
}
.legend-item { display: flex; align-items: center; gap: 6px; }
.lc {
  display: inline-block;
  width: 12px; height: 12px;
  border-radius: 3px;
}
.lc-busy    { background: #dcfce7; border: 1px solid #86efac; }
.lc-naidaku { background: #fffbeb; border: 1px solid #fde68a; }
.lc-multi   { background: #fef9c3; border: 1px solid #fde68a; }
.lc-empty   { background: #fee2e2; border: 1px solid #fca5a5; }
</style>
