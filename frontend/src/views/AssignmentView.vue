<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { getAssignments, createAssignment, updateAssignment, deleteAssignment } from '@/api/assignments'
import { getEmployees } from '@/api/employees'
import { getProjects } from '@/api/projects'
import type { Assignment, AssignmentCreate } from '@/types/assignment'
import type { Employee } from '@/types/employee'
import type { Project } from '@/types/project'

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
  } catch {
    error.value = 'データの取得に失敗しました'
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
  } catch {
    error.value = '保存に失敗しました'
  }
}

async function remove() {
  if (editingId.value === null) return
  if (!confirm('削除しますか？')) return
  try {
    await deleteAssignment(editingId.value)
    await load()
    resetForm()
  } catch {
    error.value = '削除に失敗しました'
  }
}

function statusClass(status: string): string {
  if (status === '契約期間中') return 'badge-active'
  if (status === '内諾') return 'badge-pending'
  return 'badge-done'
}

onMounted(load)
</script>

<template>
  <div class="page">
    <h2>アサイン管理</h2>
    <p v-if="error" class="error">{{ error }}</p>

    <div class="filter">
      <label>
        ステータス絞り込み
        <select v-model="statusFilter">
          <option value="">すべて</option>
          <option v-for="s in STATUSES" :key="s" :value="s">{{ s }}</option>
        </select>
      </label>
    </div>

    <table>
      <thead>
        <tr>
          <th>社員名</th><th>案件名</th><th>ランク</th><th>稼働率</th>
          <th>開始日</th><th>終了日</th><th>ステータス</th><th>単価</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="a in filteredAssignments"
          :key="a.id"
          :class="{ selected: editingId === a.id }"
          class="clickable"
          @click="selectRow(a)"
        >
          <td>{{ a.employee_name }}</td>
          <td>{{ a.project_name }}</td>
          <td>{{ a.rank ?? '' }}</td>
          <td>{{ a.utilization }}</td>
          <td>{{ a.start_date }}</td>
          <td>{{ a.end_date }}</td>
          <td><span :class="statusClass(a.status)">{{ a.status }}</span></td>
          <td>{{ a.unit_price !== null ? a.unit_price.toLocaleString() : '' }}</td>
        </tr>
      </tbody>
    </table>

    <div class="form-section">
      <h3>{{ editingId !== null ? '編集' : '新規登録' }}</h3>
      <div class="form-grid">
        <label>社員 <span class="req">*</span>
          <select v-model="form.employee_id">
            <option value="">-- 選択 --</option>
            <option v-for="e in employees" :key="e.id" :value="String(e.id)">{{ e.name }}</option>
          </select>
        </label>
        <label>案件 <span class="req">*</span>
          <select v-model="form.project_id">
            <option value="">-- 選択 --</option>
            <option v-for="p in projects" :key="p.id" :value="String(p.id)">{{ p.name }}</option>
          </select>
        </label>
        <label>枝番
          <input type="number" v-model="form.branch_no" min="1" />
        </label>
        <label>ランク
          <select v-model="form.rank">
            <option value="">-- 選択 --</option>
            <option v-for="r in RANKS" :key="r" :value="r">{{ r }}</option>
          </select>
        </label>
        <label>稼働率 <span class="req">*</span>
          <input type="number" v-model="form.utilization" min="0.05" max="1.0" step="0.05" />
        </label>
        <label>ステータス <span class="req">*</span>
          <select v-model="form.status">
            <option value="">-- 選択 --</option>
            <option v-for="s in STATUSES" :key="s" :value="s">{{ s }}</option>
          </select>
        </label>
        <label>契約開始日 <span class="req">*</span>
          <input type="date" v-model="form.start_date" />
        </label>
        <label>契約終了日 <span class="req">*</span>
          <input type="date" v-model="form.end_date" />
        </label>
        <label>単価
          <input type="number" v-model="form.unit_price" />
        </label>
        <label class="span3">メモ
          <input v-model="form.note" />
        </label>
      </div>
      <div class="actions">
        <button @click="submit">{{ editingId !== null ? '更新' : '登録' }}</button>
        <button v-if="editingId !== null" class="danger" @click="remove">削除</button>
        <button v-if="editingId !== null" @click="resetForm">キャンセル</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.page { padding: 1.5rem; }
h2 { margin-bottom: 1rem; }
.filter { margin-bottom: 1rem; }
.filter label { display: flex; flex-direction: column; font-size: 0.85rem; gap: 0.25rem; width: 12rem; }
table { border-collapse: collapse; width: 100%; margin-bottom: 1.5rem; font-size: 0.9rem; }
th, td { border: 1px solid #cbd5e1; padding: 0.4rem 0.6rem; text-align: left; }
th { background: #f1f5f9; }
.clickable { cursor: pointer; }
.clickable:hover { background: #f8fafc; }
.selected { background: #dbeafe !important; }
.form-section { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 1rem; }
h3 { margin-bottom: 0.75rem; font-size: 1rem; }
.form-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.75rem; margin-bottom: 1rem; }
.span3 { grid-column: 1 / -1; }
label { display: flex; flex-direction: column; font-size: 0.85rem; gap: 0.25rem; }
input, select { padding: 0.35rem 0.5rem; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.9rem; }
.req { color: #dc2626; }
.actions { display: flex; gap: 0.5rem; }
button { padding: 0.4rem 1rem; cursor: pointer; border: 1px solid #94a3b8; background: #fff; border-radius: 4px; }
button:hover { background: #f1f5f9; }
.danger { color: #dc2626; border-color: #dc2626; }
.danger:hover { background: #fee2e2; }
.error { color: #dc2626; margin-bottom: 0.75rem; }
.badge-active { background: #dcfce7; color: #166534; padding: 0.15rem 0.4rem; border-radius: 3px; font-size: 0.8rem; }
.badge-pending { background: #fef9c3; color: #713f12; padding: 0.15rem 0.4rem; border-radius: 3px; font-size: 0.8rem; }
.badge-done { background: #f1f5f9; color: #475569; padding: 0.15rem 0.4rem; border-radius: 3px; font-size: 0.8rem; }
</style>
