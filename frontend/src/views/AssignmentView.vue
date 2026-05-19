<script setup lang="ts">
import { extractError } from '@/api/client'
import { ref, reactive, computed, onMounted } from 'vue'
import { getAssignments, createAssignment, updateAssignment, deleteAssignment } from '@/api/assignments'
import { getEmployees } from '@/api/employees'
import { getProjects } from '@/api/projects'
import type { Assignment, AssignmentCreate } from '@/types/assignment'
import type { Employee } from '@/types/employee'
import type { Project } from '@/types/project'
import { downloadCsv } from '@/utils/csv'

const RANKS = ['アナリスト', 'コンサルタント', 'シニアコンサルタント', 'マネージャー', 'シニアマネージャー', 'ディレクター', 'パートナー']
const STATUSES = ['契約期間中', '内諾', '完了']

const assignments = ref<Assignment[]>([])
const employees = ref<Employee[]>([])
const projects = ref<Project[]>([])
const editingId = ref<number | null>(null)
const statusFilter = ref('')
const error = ref('')

const filteredAssignments = computed(() =>
  statusFilter.value === ''
    ? assignments.value
    : assignments.value.filter(a => a.status === statusFilter.value)
)

const form = reactive({
  employee_id: '',
  project_id: '',
  branch_no: '',
  rank: '',
  utilization: '1.0',
  start_date: '',
  end_date: '',
  status: '',
  unit_price: '',
  note: '',
})

function resetForm() {
  editingId.value = null
  form.employee_id = ''
  form.project_id = ''
  form.branch_no = ''
  form.rank = ''
  form.utilization = '1.0'
  form.start_date = ''
  form.end_date = ''
  form.status = ''
  form.unit_price = ''
  form.note = ''
}

function selectRow(a: Assignment) {
  editingId.value = a.id
  form.employee_id = String(a.employee_id)
  form.project_id = String(a.project_id)
  form.branch_no = a.branch_no !== null ? String(a.branch_no) : ''
  form.rank = a.rank ?? ''
  form.utilization = String(a.utilization)
  form.start_date = a.start_date
  form.end_date = a.end_date
  form.status = a.status
  form.unit_price = a.unit_price !== null ? String(a.unit_price) : ''
  form.note = a.note ?? ''
}

async function load() {
  try {
    const [asn, emp, prj] = await Promise.all([getAssignments(), getEmployees(), getProjects()])
    assignments.value = asn
    employees.value = emp
    projects.value = prj
  } catch (e) {
    error.value = extractError(e)
  }
}

function toIntOrNull(val: string): number | null {
  const n = parseInt(val, 10)
  return val === '' || isNaN(n) ? null : n
}

async function submit() {
  if (!form.employee_id || !form.project_id || !form.utilization || !form.start_date || !form.end_date || !form.status) {
    error.value = '必須項目を入力してください'
    return
  }
  const util = Number(form.utilization)
  if (isNaN(util) || util <= 0 || util > 1.0) {
    error.value = '稼働率は 0 より大きく 1.0 以下の値を入力してください'
    return
  }
  if (form.start_date > form.end_date) {
    error.value = '開始日は終了日以前の日付を入力してください'
    return
  }
  const price = form.unit_price ? Number(form.unit_price) : null
  if (price !== null && price < 0) {
    error.value = '単価は 0 以上の値を入力してください'
    return
  }
  error.value = ''
  const body: AssignmentCreate = {
    employee_id: Number(form.employee_id),
    project_id: Number(form.project_id),
    branch_no: toIntOrNull(form.branch_no),
    rank: form.rank || null,
    utilization: Number(form.utilization),
    start_date: form.start_date,
    end_date: form.end_date,
    status: form.status,
    unit_price: toIntOrNull(form.unit_price),
    note: form.note || null,
  }
  try {
    if (editingId.value !== null) {
      await updateAssignment(editingId.value, body)
    } else {
      await createAssignment(body)
    }
    await load()
    resetForm()
  } catch (e) {
    error.value = extractError(e)
  }
}

async function remove() {
  if (editingId.value === null) return
  if (!confirm('削除しますか？')) return
  try {
    await deleteAssignment(editingId.value)
    await load()
    resetForm()
  } catch (e) {
    error.value = extractError(e)
  }
}

function statusBadgeClass(status: string): string {
  if (status === '契約期間中') return 'badge badge-active'
  if (status === '内諾') return 'badge badge-pending'
  return 'badge badge-done'
}

function exportCsv() {
  const headers = ['社員名', '案件名', 'ランク', '稼働率', '開始日', '終了日', 'ステータス', '単価', 'メモ']
  const rows = filteredAssignments.value.map(a => [
    a.employee_name,
    a.project_name,
    a.rank ?? '',
    `${Math.round(a.utilization * 100)}%`,
    a.start_date,
    a.end_date,
    a.status,
    a.unit_price !== null ? String(a.unit_price) : '',
    a.note ?? '',
  ])
  const suffix = statusFilter.value ? `_${statusFilter.value}` : ''
  downloadCsv(headers, rows, `アサイン一覧${suffix}.csv`)
}

onMounted(load)
</script>

<template>
  <div class="page">
    <div class="page-header">
      <div>
        <div class="page-title">
          アサイン管理
          <span class="count-badge">{{ filteredAssignments.length }}</span>
        </div>
        <div class="page-desc">社員と案件のアサイン登録・管理</div>
      </div>
      <button class="btn btn-primary" @click="resetForm">
        <svg viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd"/></svg>
        アサインを追加
      </button>
    </div>

    <div v-if="error" class="error-banner">
      <svg viewBox="0 0 20 20" fill="currentColor" style="width:16px;height:16px;flex-shrink:0;margin-top:1px"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/></svg>
      {{ error }}
    </div>

    <div class="filter-bar">
      <span class="filter-label">ステータス</span>
      <button
        class="filter-btn"
        :class="{ active: statusFilter === '' }"
        @click="statusFilter = ''"
      >すべて</button>
      <button
        v-for="s in STATUSES"
        :key="s"
        class="filter-btn"
        :class="{ active: statusFilter === s }"
        @click="statusFilter = s"
      >{{ s }}</button>
      <span style="flex:1"></span>
      <button class="btn btn-secondary btn-sm" @click="exportCsv">
        <svg viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clip-rule="evenodd"/></svg>
        CSV出力
      </button>
    </div>

    <div class="card" style="overflow:hidden;margin-bottom:20px">
      <table class="data-table">
        <thead>
          <tr>
            <th>社員名</th>
            <th>案件名</th>
            <th>ランク</th>
            <th>稼働率</th>
            <th>開始日</th>
            <th>終了日</th>
            <th>ステータス</th>
            <th>単価</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="a in filteredAssignments"
            :key="a.id"
            class="row-clickable"
            :class="{ 'row-selected': editingId === a.id }"
            @click="selectRow(a)"
          >
            <td style="font-weight:500">{{ a.employee_name }}</td>
            <td>{{ a.project_name }}</td>
            <td>{{ a.rank ?? '' }}</td>
            <td>{{ Math.round(a.utilization * 100) }}%</td>
            <td class="nowrap">{{ a.start_date }}</td>
            <td class="nowrap">{{ a.end_date }}</td>
            <td><span :class="statusBadgeClass(a.status)">{{ a.status }}</span></td>
            <td class="text-right">{{ a.unit_price !== null ? a.unit_price.toLocaleString() : '' }}</td>
          </tr>
          <tr v-if="filteredAssignments.length === 0">
            <td colspan="8" class="empty-state">アサインが登録されていません</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="card">
      <div class="card-header">
        <span class="card-title">{{ editingId !== null ? 'アサインを編集' : '新規登録' }}</span>
        <button v-if="editingId !== null" class="btn btn-ghost btn-sm" @click="resetForm">キャンセル</button>
      </div>
      <div class="card-body">
        <div class="form-grid">
          <div class="field">
            <label>社員<span class="req">*</span></label>
            <select v-model="form.employee_id">
              <option value="">-- 選択 --</option>
              <option v-for="e in employees" :key="e.id" :value="String(e.id)">{{ e.name }}</option>
            </select>
          </div>
          <div class="field span2">
            <label>案件<span class="req">*</span></label>
            <select v-model="form.project_id">
              <option value="">-- 選択 --</option>
              <option v-for="p in projects" :key="p.id" :value="String(p.id)">{{ p.name }}</option>
            </select>
          </div>
          <div class="field">
            <label>枝番</label>
            <input type="number" v-model="form.branch_no" min="1" placeholder="1" />
          </div>
          <div class="field">
            <label>ランク</label>
            <select v-model="form.rank">
              <option value="">-- 選択 --</option>
              <option v-for="r in RANKS" :key="r" :value="r">{{ r }}</option>
            </select>
          </div>
          <div class="field">
            <label>稼働率<span class="req">*</span></label>
            <input type="number" v-model="form.utilization" min="0.05" max="1.0" step="0.05" placeholder="1.0" />
          </div>
          <div class="field">
            <label>ステータス<span class="req">*</span></label>
            <select v-model="form.status">
              <option value="">-- 選択 --</option>
              <option v-for="s in STATUSES" :key="s" :value="s">{{ s }}</option>
            </select>
          </div>
          <div class="field">
            <label>契約開始日<span class="req">*</span></label>
            <input type="date" v-model="form.start_date" />
          </div>
          <div class="field">
            <label>契約終了日<span class="req">*</span></label>
            <input type="date" v-model="form.end_date" />
          </div>
          <div class="field">
            <label>単価</label>
            <input type="number" v-model="form.unit_price" placeholder="0" />
          </div>
          <div class="field span3">
            <label>メモ</label>
            <input v-model="form.note" placeholder="メモ・備考など" />
          </div>
        </div>
        <div class="form-actions">
          <button class="btn btn-primary" @click="submit">
            {{ editingId !== null ? '更新する' : '登録する' }}
          </button>
          <button v-if="editingId !== null" class="btn btn-danger" @click="remove">削除</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.filter-bar {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 16px;
}
.filter-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-3);
  margin-right: 4px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.filter-btn {
  padding: 5px 12px;
  border-radius: 20px;
  border: 1px solid var(--border-strong);
  background: var(--surface);
  color: var(--text-2);
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: background 0.1s, color 0.1s, border-color 0.1s;
  font-family: inherit;
}
.filter-btn:hover { background: var(--surface-sub); }
.filter-btn.active {
  background: var(--primary);
  border-color: var(--primary);
  color: #fff;
}
.nowrap { white-space: nowrap; }
</style>
