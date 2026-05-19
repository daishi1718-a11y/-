<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { extractError } from '@/api/client'
import { getEmployees } from '@/api/employees'
import { getClients } from '@/api/clients'
import { getProjects } from '@/api/projects'
import { getAssignments } from '@/api/assignments'
import { getStaffingMatrix } from '@/api/staffing'
import type { Employee } from '@/types/employee'
import type { Assignment } from '@/types/assignment'
import type { Project } from '@/types/project'
import type { StaffingMatrix, StaffingCell } from '@/types/staffing'

const employees = ref<Employee[]>([])
const assignments = ref<Assignment[]>([])
const projects = ref<Project[]>([])
const matrix = ref<StaffingMatrix | null>(null)
const error = ref('')

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

const activeEmployeeCount = computed(() =>
  employees.value.filter(e => e.status !== '退職').length
)

const contractCount = computed(() =>
  assignments.value.filter(a => a.status === '契約期間中').length
)

const naidakuCount = computed(() =>
  assignments.value.filter(a => a.status === '内諾').length
)

const recentAssignments = computed(() =>
  assignments.value
    .filter(a => a.status !== '完了')
    .slice(0, 6)
)

function statusBadgeClass(status: string): string {
  if (status === '契約期間中') return 'badge badge-active'
  if (status === '内諾') return 'badge badge-pending'
  return 'badge badge-done'
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

const snapshotMonths = computed(() => {
  const from = currentYearMonth()
  return [from, addMonths(from, 1), addMonths(from, 2)]
})

onMounted(async () => {
  try {
    const [emp, , prj, asn] = await Promise.all([
      getEmployees(),
      getClients(),
      getProjects(),
      getAssignments(),
    ])
    employees.value = emp
    projects.value = prj
    assignments.value = asn

    const from = currentYearMonth()
    const to = addMonths(from, 2)
    matrix.value = await getStaffingMatrix(from, to)
  } catch (e) {
    error.value = extractError(e)
  }
})
</script>

<template>
  <div class="page">
    <div class="page-header">
      <div>
        <div class="page-title">ダッシュボード</div>
        <div class="page-desc">要員・案件・アサインの概況</div>
      </div>
    </div>

    <div v-if="error" class="error-banner">
      <svg viewBox="0 0 20 20" fill="currentColor" style="width:16px;height:16px;flex-shrink:0;margin-top:1px"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/></svg>
      {{ error }}
    </div>

    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-label">在籍社員</div>
        <div class="stat-value">{{ activeEmployeeCount }}</div>
        <div class="stat-sub">退職者除く</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">契約期間中</div>
        <div class="stat-value stat-green">{{ contractCount }}</div>
        <div class="stat-sub">アサイン件数</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">内諾</div>
        <div class="stat-value stat-amber">{{ naidakuCount }}</div>
        <div class="stat-sub">アサイン件数</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">登録案件</div>
        <div class="stat-value">{{ projects.length }}</div>
        <div class="stat-sub">累計</div>
      </div>
    </div>

    <div class="dash-grid">
      <!-- Recent assignments -->
      <div class="card" style="overflow:hidden">
        <div class="card-header">
          <span class="card-title">直近のアサイン</span>
          <RouterLink to="/assignments" class="btn btn-ghost btn-sm">すべて表示</RouterLink>
        </div>
        <table class="data-table">
          <thead>
            <tr>
              <th>社員</th>
              <th>案件</th>
              <th>期間</th>
              <th>稼働率</th>
              <th>ステータス</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="a in recentAssignments" :key="a.id">
              <td>{{ a.employee_name }}</td>
              <td>{{ a.project_name }}</td>
              <td class="nowrap">{{ a.start_date }} 〜 {{ a.end_date }}</td>
              <td>{{ Math.round(a.utilization * 100) }}%</td>
              <td><span :class="statusBadgeClass(a.status)">{{ a.status }}</span></td>
            </tr>
            <tr v-if="recentAssignments.length === 0">
              <td colspan="5" class="empty-state">データがありません</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Staffing snapshot -->
      <div class="card" style="overflow:hidden">
        <div class="card-header">
          <span class="card-title">稼働スナップショット（3ヶ月）</span>
          <RouterLink to="/staffing" class="btn btn-ghost btn-sm">詳細</RouterLink>
        </div>
        <div v-if="matrix" style="overflow-x:auto">
          <table class="data-table matrix-table">
            <thead>
              <tr>
                <th style="text-align:left;min-width:120px">社員名</th>
                <th v-for="m in snapshotMonths" :key="m" style="text-align:center;min-width:72px">{{ monthLabel(m) }}</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in matrix.rows" :key="row.employee_id">
                <td style="font-weight:500">{{ row.employee_name }}</td>
                <td
                  v-for="m in snapshotMonths"
                  :key="m"
                  :class="cellClass(row.cells[m])"
                  :title="row.cells[m]?.project_name ?? ''"
                  style="text-align:center;font-size:11px;font-weight:600"
                >
                  {{ cellLabel(row.cells[m]) }}
                </td>
              </tr>
              <tr v-if="!matrix.rows.length">
                <td colspan="4" class="empty-state">データがありません</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-else class="empty-state">読み込み中...</div>

        <div class="legend">
          <span class="legend-item"><span class="lc lc-busy"></span>契約期間中</span>
          <span class="legend-item"><span class="lc lc-naidaku"></span>内諾</span>
          <span class="legend-item"><span class="lc lc-multi"></span>複数</span>
          <span class="legend-item"><span class="lc lc-empty"></span>空き</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}
.stat-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  padding: 20px 24px;
}
.stat-label { font-size: 12px; font-weight: 600; color: var(--text-3); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px; }
.stat-value { font-size: 32px; font-weight: 700; color: var(--text); line-height: 1; margin-bottom: 4px; }
.stat-value.stat-green { color: var(--green); }
.stat-value.stat-amber { color: var(--amber); }
.stat-sub { font-size: 12px; color: var(--text-3); }

.dash-grid {
  display: grid;
  grid-template-columns: 1.3fr 0.7fr;
  gap: 16px;
  align-items: start;
}

/* matrix cell colors */
.mc-busy    { background: #dcfce7; color: #166534; }
.mc-naidaku { background: #fffbeb; color: #78350f; }
.mc-multi   { background: #fef9c3; color: #713f12; }
.mc-empty   { background: #fee2e2; color: #991b1b; }

.legend {
  display: flex;
  gap: 16px;
  padding: 12px 16px;
  border-top: 1px solid var(--border);
  font-size: 11px;
  color: var(--text-2);
}
.legend-item { display: flex; align-items: center; gap: 5px; }
.lc {
  display: inline-block;
  width: 10px; height: 10px;
  border-radius: 2px;
}
.lc-busy    { background: #dcfce7; border: 1px solid #86efac; }
.lc-naidaku { background: #fffbeb; border: 1px solid #fde68a; }
.lc-multi   { background: #fef9c3; border: 1px solid #fde68a; }
.lc-empty   { background: #fee2e2; border: 1px solid #fca5a5; }
</style>
