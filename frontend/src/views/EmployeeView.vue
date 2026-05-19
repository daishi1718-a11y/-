<script setup lang="ts">
import { extractError } from '@/api/client'
import { ref, reactive, computed, onMounted } from 'vue'
import { getEmployees, createEmployee, updateEmployee, deleteEmployee } from '@/api/employees'
import type { Employee, EmployeeCreate } from '@/types/employee'

const POSITIONS = ['アナリスト', 'コンサルタント', 'シニアコンサルタント', 'マネージャー', 'シニアマネージャー', 'ディレクター', 'パートナー']
const STATUSES = ['在籍', '退職', '入社見込み']

const employees = ref<Employee[]>([])
const editingId = ref<number | null>(null)
const statusFilter = ref('')
const error = ref('')

const filteredEmployees = computed(() =>
  statusFilter.value === ''
    ? employees.value
    : employees.value.filter(e => e.status === statusFilter.value)
)

const form = reactive({
  employee_code: '',
  name: '',
  position: '',
  status: '',
  joined_at: '',
  left_at: '',
})

function resetForm() {
  editingId.value = null
  form.employee_code = ''
  form.name = ''
  form.position = ''
  form.status = ''
  form.joined_at = ''
  form.left_at = ''
}

function selectRow(emp: Employee) {
  editingId.value = emp.id
  form.employee_code = emp.employee_code
  form.name = emp.name
  form.position = emp.position
  form.status = emp.status
  form.joined_at = emp.joined_at ?? ''
  form.left_at = emp.left_at ?? ''
}

async function load() {
  try {
    employees.value = await getEmployees()
  } catch (e) {
    error.value = extractError(e)
  }
}

async function submit() {
  if (!form.employee_code || !form.name || !form.position || !form.status) {
    error.value = '必須項目を入力してください'
    return
  }
  error.value = ''
  const body: EmployeeCreate = {
    employee_code: form.employee_code,
    name: form.name,
    position: form.position,
    status: form.status,
    joined_at: form.joined_at || null,
    left_at: form.left_at || null,
  }
  try {
    if (editingId.value !== null) {
      await updateEmployee(editingId.value, body)
    } else {
      await createEmployee(body)
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
    await deleteEmployee(editingId.value)
    await load()
    resetForm()
  } catch (e) {
    error.value = extractError(e)
  }
}

function statusBadgeClass(status: string): string {
  if (status === '在籍') return 'badge badge-active'
  if (status === '入社見込み') return 'badge badge-info'
  return 'badge badge-done'
}

onMounted(load)
</script>

<template>
  <div class="page">
    <div class="page-header">
      <div>
        <div class="page-title">
          社員管理
          <span class="count-badge">{{ filteredEmployees.length }}</span>
        </div>
        <div class="page-desc">社員マスタの登録・編集</div>
      </div>
      <button class="btn btn-primary" @click="resetForm">
        <svg viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd"/></svg>
        社員を追加
      </button>
    </div>

    <div v-if="error" class="error-banner">
      <svg viewBox="0 0 20 20" fill="currentColor" style="width:16px;height:16px;flex-shrink:0;margin-top:1px"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/></svg>
      {{ error }}
    </div>

    <div class="filter-bar">
      <span class="filter-label">在籍状況</span>
      <button class="filter-btn" :class="{ active: statusFilter === '' }" @click="statusFilter = ''">すべて</button>
      <button v-for="s in STATUSES" :key="s" class="filter-btn" :class="{ active: statusFilter === s }" @click="statusFilter = s">{{ s }}</button>
    </div>

    <div class="card" style="overflow:hidden;margin-bottom:20px">
      <table class="data-table">
        <thead>
          <tr>
            <th>社員番号</th>
            <th>氏名</th>
            <th>クラス</th>
            <th>在籍状況</th>
            <th>入社日</th>
            <th>退職日</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="emp in filteredEmployees"
            :key="emp.id"
            class="row-clickable"
            :class="{ 'row-selected': editingId === emp.id }"
            @click="selectRow(emp)"
          >
            <td class="text-mono">{{ emp.employee_code }}</td>
            <td style="font-weight:500">{{ emp.name }}</td>
            <td>{{ emp.position }}</td>
            <td><span :class="statusBadgeClass(emp.status)">{{ emp.status }}</span></td>
            <td class="nowrap">{{ emp.joined_at ?? '' }}</td>
            <td class="nowrap">{{ emp.left_at ?? '' }}</td>
          </tr>
          <tr v-if="filteredEmployees.length === 0">
            <td colspan="6" class="empty-state">{{ statusFilter ? '該当する社員がいません' : '社員が登録されていません' }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="card">
      <div class="card-header">
        <span class="card-title">{{ editingId !== null ? '社員を編集' : '新規登録' }}</span>
        <button v-if="editingId !== null" class="btn btn-ghost btn-sm" @click="resetForm">キャンセル</button>
      </div>
      <div class="card-body">
        <div class="form-grid">
          <div class="field">
            <label>社員番号<span class="req">*</span></label>
            <input v-model="form.employee_code" placeholder="EMP001" />
          </div>
          <div class="field">
            <label>氏名<span class="req">*</span></label>
            <input v-model="form.name" placeholder="山田 太郎" />
          </div>
          <div class="field">
            <label>クラス<span class="req">*</span></label>
            <select v-model="form.position">
              <option value="">-- 選択 --</option>
              <option v-for="p in POSITIONS" :key="p" :value="p">{{ p }}</option>
            </select>
          </div>
          <div class="field">
            <label>在籍状況<span class="req">*</span></label>
            <select v-model="form.status">
              <option value="">-- 選択 --</option>
              <option v-for="s in STATUSES" :key="s" :value="s">{{ s }}</option>
            </select>
          </div>
          <div class="field">
            <label>入社日</label>
            <input type="date" v-model="form.joined_at" />
          </div>
          <div class="field">
            <label>退職日</label>
            <input type="date" v-model="form.left_at" />
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
.nowrap { white-space: nowrap; }

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
</style>
