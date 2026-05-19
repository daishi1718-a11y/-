<script setup lang="ts">
import { extractError } from '@/api/client'
import { ref, reactive, onMounted } from 'vue'
import { getEmployees, createEmployee, updateEmployee, deleteEmployee } from '@/api/employees'
import type { Employee, EmployeeCreate } from '@/types/employee'

const POSITIONS = ['アナリスト', 'コンサルタント', 'シニアコンサルタント', 'マネージャー', 'シニアマネージャー', 'ディレクター', 'パートナー']
const STATUSES = ['在籍', '退職', '入社見込み']

const employees = ref<Employee[]>([])
const editingId = ref<number | null>(null)
const error = ref('')

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

onMounted(load)
</script>

<template>
  <div class="page">
    <h2>社員管理</h2>
    <p v-if="error" class="error">{{ error }}</p>

    <table>
      <thead>
        <tr>
          <th>社員番号</th><th>氏名</th><th>クラス</th><th>在籍状況</th><th>入社日</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="emp in employees"
          :key="emp.id"
          :class="{ selected: editingId === emp.id }"
          class="clickable"
          @click="selectRow(emp)"
        >
          <td>{{ emp.employee_code }}</td>
          <td>{{ emp.name }}</td>
          <td>{{ emp.position }}</td>
          <td>{{ emp.status }}</td>
          <td>{{ emp.joined_at ?? '' }}</td>
        </tr>
      </tbody>
    </table>

    <div class="form-section">
      <h3>{{ editingId !== null ? '編集' : '新規登録' }}</h3>
      <div class="form-grid">
        <label>社員番号 <span class="req">*</span>
          <input v-model="form.employee_code" />
        </label>
        <label>氏名 <span class="req">*</span>
          <input v-model="form.name" />
        </label>
        <label>クラス <span class="req">*</span>
          <select v-model="form.position">
            <option value="">-- 選択 --</option>
            <option v-for="p in POSITIONS" :key="p" :value="p">{{ p }}</option>
          </select>
        </label>
        <label>在籍状況 <span class="req">*</span>
          <select v-model="form.status">
            <option value="">-- 選択 --</option>
            <option v-for="s in STATUSES" :key="s" :value="s">{{ s }}</option>
          </select>
        </label>
        <label>入社日
          <input type="date" v-model="form.joined_at" />
        </label>
        <label>退職日
          <input type="date" v-model="form.left_at" />
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
table { border-collapse: collapse; width: 100%; margin-bottom: 1.5rem; font-size: 0.9rem; }
th, td { border: 1px solid #cbd5e1; padding: 0.4rem 0.6rem; text-align: left; }
th { background: #f1f5f9; }
.clickable { cursor: pointer; }
.clickable:hover { background: #f8fafc; }
.selected { background: #dbeafe !important; }
.form-section { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 1rem; }
h3 { margin-bottom: 0.75rem; font-size: 1rem; }
.form-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.75rem; margin-bottom: 1rem; }
label { display: flex; flex-direction: column; font-size: 0.85rem; gap: 0.25rem; }
input, select { padding: 0.35rem 0.5rem; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.9rem; }
.req { color: #dc2626; }
.actions { display: flex; gap: 0.5rem; }
button { padding: 0.4rem 1rem; cursor: pointer; border: 1px solid #94a3b8; background: #fff; border-radius: 4px; }
button:hover { background: #f1f5f9; }
.danger { color: #dc2626; border-color: #dc2626; }
.danger:hover { background: #fee2e2; }
.error { color: #dc2626; margin-bottom: 0.75rem; }
</style>
