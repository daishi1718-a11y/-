<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { getProjects, createProject, updateProject, deleteProject } from '@/api/projects'
import { getClients } from '@/api/clients'
import type { Project, ProjectCreate } from '@/types/project'
import type { Client } from '@/types/client'

const ROLES = ['PM/PMO', '企画・推進', '社員代替']
const PROCESSES = ['戦略・企画', '計画策定', '要件定義', '設計', '開発', 'テスト', '移行', '運用・保守', 'その他']

const projects = ref<Project[]>([])
const clients = ref<Client[]>([])
const editingId = ref<number | null>(null)
const error = ref('')

const form = reactive({
  project_code: '',
  name: '',
  description: '',
  role: '',
  required_skill: '',
  preferred_skill: '',
  process_flags: [] as string[],
  end_client_id: '',
  prime_client_id: '',
  mid1_client_id: '',
  mid2_client_id: '',
  contract_client_id: '',
})

function clientName(id: number | null): string {
  if (id === null) return ''
  const found = clients.value.find(c => c.id === id)
  return found ? found.name : ''
}

function toIdOrNull(val: string): number | null {
  const n = Number(val)
  return val === '' || isNaN(n) ? null : n
}

function resetForm() {
  editingId.value = null
  form.project_code = ''
  form.name = ''
  form.description = ''
  form.role = ''
  form.required_skill = ''
  form.preferred_skill = ''
  form.process_flags = []
  form.end_client_id = ''
  form.prime_client_id = ''
  form.mid1_client_id = ''
  form.mid2_client_id = ''
  form.contract_client_id = ''
}

function selectRow(p: Project) {
  editingId.value = p.id
  form.project_code = p.project_code
  form.name = p.name
  form.description = p.description ?? ''
  form.role = p.role ?? ''
  form.required_skill = p.required_skill ?? ''
  form.preferred_skill = p.preferred_skill ?? ''
  form.process_flags = p.process_flags ? p.process_flags.split(',') : []
  form.end_client_id = p.end_client_id !== null ? String(p.end_client_id) : ''
  form.prime_client_id = p.prime_client_id !== null ? String(p.prime_client_id) : ''
  form.mid1_client_id = p.mid1_client_id !== null ? String(p.mid1_client_id) : ''
  form.mid2_client_id = p.mid2_client_id !== null ? String(p.mid2_client_id) : ''
  form.contract_client_id = p.contract_client_id !== null ? String(p.contract_client_id) : ''
}

async function load() {
  try {
    const [prj, cli] = await Promise.all([getProjects(), getClients()])
    projects.value = prj
    clients.value = cli
  } catch {
    error.value = 'データの取得に失敗しました'
  }
}

async function submit() {
  if (!form.project_code || !form.name) {
    error.value = '必須項目を入力してください'
    return
  }
  error.value = ''
  const body: ProjectCreate = {
    project_code: form.project_code,
    name: form.name,
    description: form.description || null,
    role: form.role || null,
    required_skill: form.required_skill || null,
    preferred_skill: form.preferred_skill || null,
    process_flags: form.process_flags.length > 0 ? form.process_flags.join(',') : null,
    end_client_id: toIdOrNull(form.end_client_id),
    prime_client_id: toIdOrNull(form.prime_client_id),
    mid1_client_id: toIdOrNull(form.mid1_client_id),
    mid2_client_id: toIdOrNull(form.mid2_client_id),
    contract_client_id: toIdOrNull(form.contract_client_id),
  }
  try {
    if (editingId.value !== null) {
      await updateProject(editingId.value, body)
    } else {
      await createProject(body)
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
    await deleteProject(editingId.value)
    await load()
    resetForm()
  } catch {
    error.value = '削除に失敗しました'
  }
}

onMounted(load)
</script>

<template>
  <div class="page">
    <h2>案件管理</h2>
    <p v-if="error" class="error">{{ error }}</p>

    <table>
      <thead>
        <tr>
          <th>案件コード</th><th>案件名</th><th>役割</th><th>エンド顧客</th><th>契約企業</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="p in projects"
          :key="p.id"
          :class="{ selected: editingId === p.id }"
          class="clickable"
          @click="selectRow(p)"
        >
          <td>{{ p.project_code }}</td>
          <td>{{ p.name }}</td>
          <td>{{ p.role ?? '' }}</td>
          <td>{{ clientName(p.end_client_id) }}</td>
          <td>{{ clientName(p.contract_client_id) }}</td>
        </tr>
      </tbody>
    </table>

    <div class="form-section">
      <h3>{{ editingId !== null ? '編集' : '新規登録' }}</h3>
      <div class="form-grid">
        <label>案件コード <span class="req">*</span>
          <input v-model="form.project_code" />
        </label>
        <label>案件名 <span class="req">*</span>
          <input v-model="form.name" />
        </label>
        <label>役割
          <select v-model="form.role">
            <option value="">-- 選択 --</option>
            <option v-for="r in ROLES" :key="r" :value="r">{{ r }}</option>
          </select>
        </label>
        <label class="span2">概要
          <input v-model="form.description" />
        </label>
        <label>必要スキル
          <input v-model="form.required_skill" />
        </label>
        <label>歓迎スキル
          <input v-model="form.preferred_skill" />
        </label>
        <label>エンド顧客
          <select v-model="form.end_client_id">
            <option value="">-- 選択 --</option>
            <option v-for="c in clients" :key="c.id" :value="String(c.id)">{{ c.name }}</option>
          </select>
        </label>
        <label>プライム
          <select v-model="form.prime_client_id">
            <option value="">-- 選択 --</option>
            <option v-for="c in clients" :key="c.id" :value="String(c.id)">{{ c.name }}</option>
          </select>
        </label>
        <label>中間1
          <select v-model="form.mid1_client_id">
            <option value="">-- 選択 --</option>
            <option v-for="c in clients" :key="c.id" :value="String(c.id)">{{ c.name }}</option>
          </select>
        </label>
        <label>中間2
          <select v-model="form.mid2_client_id">
            <option value="">-- 選択 --</option>
            <option v-for="c in clients" :key="c.id" :value="String(c.id)">{{ c.name }}</option>
          </select>
        </label>
        <label>契約企業
          <select v-model="form.contract_client_id">
            <option value="">-- 選択 --</option>
            <option v-for="c in clients" :key="c.id" :value="String(c.id)">{{ c.name }}</option>
          </select>
        </label>
        <div class="process-wrap">
          <span class="label-text">想定工程</span>
          <div class="checkboxes">
            <label v-for="proc in PROCESSES" :key="proc" class="inline">
              <input type="checkbox" :value="proc" v-model="form.process_flags" /> {{ proc }}
            </label>
          </div>
        </div>
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
.span2 { grid-column: span 2; }
label { display: flex; flex-direction: column; font-size: 0.85rem; gap: 0.25rem; }
label.inline { flex-direction: row; align-items: center; gap: 0.3rem; font-size: 0.85rem; }
input, select { padding: 0.35rem 0.5rem; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.9rem; }
.req { color: #dc2626; }
.process-wrap { grid-column: 1 / -1; }
.label-text { font-size: 0.85rem; display: block; margin-bottom: 0.25rem; }
.checkboxes { display: flex; flex-wrap: wrap; gap: 0.5rem; }
.actions { display: flex; gap: 0.5rem; }
button { padding: 0.4rem 1rem; cursor: pointer; border: 1px solid #94a3b8; background: #fff; border-radius: 4px; }
button:hover { background: #f1f5f9; }
.danger { color: #dc2626; border-color: #dc2626; }
.danger:hover { background: #fee2e2; }
.error { color: #dc2626; margin-bottom: 0.75rem; }
</style>
