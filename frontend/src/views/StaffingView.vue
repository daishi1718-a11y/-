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
  if (!cell || cell.status === '空き') return 'cell-empty'
  if (cell.count > 1) return 'cell-multi'
  return 'cell-busy'
}

function cellLabel(cell: StaffingCell | undefined): string {
  if (!cell || cell.status === '空き') return ''
  if (cell.count > 1) return `×${cell.count}`
  return '■'
}

onMounted(load)
</script>

<template>
  <div class="page">
    <h2>稼働マトリクス</h2>

    <div class="filter">
      <label>
        表示開始月
        <input type="month" v-model="fromMonth" />
      </label>
      <label>
        表示終了月
        <input type="month" v-model="toMonth" />
      </label>
      <button @click="load">表示</button>
    </div>

    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="loading">読み込み中...</p>

    <div v-if="matrix" class="table-wrap">
      <table>
        <thead>
          <tr>
            <th class="name-col">社員名</th>
            <th v-for="m in matrix.months" :key="m">{{ m }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in matrix.rows" :key="row.employee_id">
            <td class="name-col">{{ row.employee_name }}</td>
            <td
              v-for="m in matrix.months"
              :key="m"
              :class="cellClass(row.cells[m])"
              :title="row.cells[m]?.project_name ?? ''"
            >
              {{ cellLabel(row.cells[m]) }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.page {
  padding: 1.5rem;
}
h2 {
  margin-bottom: 1rem;
}
.filter {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}
.filter label {
  display: flex;
  flex-direction: column;
  font-size: 0.85rem;
  gap: 0.25rem;
}
.filter button {
  align-self: flex-end;
  padding: 0.4rem 1rem;
  cursor: pointer;
}
.table-wrap {
  overflow-x: auto;
}
table {
  border-collapse: collapse;
  min-width: 100%;
  font-size: 0.9rem;
}
th, td {
  border: 1px solid #cbd5e1;
  padding: 0.4rem 0.6rem;
  text-align: center;
  white-space: nowrap;
}
.name-col {
  text-align: left;
  min-width: 8rem;
}
.cell-busy {
  background: #dcfce7;
  color: #166534;
  font-weight: bold;
}
.cell-empty {
  background: #fee2e2;
}
.cell-multi {
  background: #fef9c3;
  color: #713f12;
  font-weight: bold;
}
.error {
  color: #dc2626;
}
</style>
