<script setup lang="ts">
import { extractError } from '@/api/client'
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
  } catch (e) {
    error.value = extractError(e)
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
  } catch (e) {
    error.value = extractError(e)
  }
}

async function remove() {
  if (editingId.value === null) return
  if (!confirm('削除しますか？')) return
  try {
    await deleteProject(editingId.value)
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
    <div class="page-header">
      <div>
        <div class="page-title">
          案件管理
          <span class="count-badge">{{ projects.length }}</span>
        </div>
        <div class="page-desc">案件マスタの登録・編集</div>
      </div>
      <button class="btn btn-primary" @click="resetForm">
        <svg viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd"/></svg>
        案件を追加
      </button>
    </div>

    <div v-if="error" class="error-banner">
      <svg viewBox="0 0 20 20" fill="currentColor" style="width:16px;height:16px;flex-shrink:0;margin-top:1px"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/></svg>
      {{ error }}
    </div>

    <div class="card" style="overflow:hidden;margin-bottom:20px">
      <table class="data-table">
        <thead>
          <tr>
            <th>案件コード</th>
            <th>案件名</th>
            <th>役割</th>
            <th>エンド顧客</th>
            <th>契約企業</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="p in projects"
            :key="p.id"
            class="row-clickable"
            :class="{ 'row-selected': editingId === p.id }"
            @click="selectRow(p)"
          >
            <td class="text-mono">{{ p.project_code }}</td>
            <td style="font-weight:500">{{ p.name }}</td>
            <td>{{ p.role ?? '' }}</td>
            <td>{{ clientName(p.end_client_id) }}</td>
            <td>{{ clientName(p.contract_client_id) }}</td>
          </tr>
          <tr v-if="projects.length === 0">
            <td colspan="5" class="empty-state">案件が登録されていません</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="card">
      <div class="card-header">
        <span class="card-title">{{ editingId !== null ? '案件を編集' : '新規登録' }}</span>
        <button v-if="editingId !== null" class="btn btn-ghost btn-sm" @click="resetForm">キャンセル</button>
      </div>
      <div class="card-body">
        <div class="form-grid">
          <div class="field">
            <label>案件コード<span class="req">*</span></label>
            <input v-model="form.project_code" placeholder="PRJ001" />
          </div>
          <div class="field span2">
            <label>案件名<span class="req">*</span></label>
            <input v-model="form.name" placeholder="〇〇システム開発支援" />
          </div>
          <div class="field">
            <label>役割</label>
            <select v-model="form.role">
              <option value="">-- 選択 --</option>
              <option v-for="r in ROLES" :key="r" :value="r">{{ r }}</option>
            </select>
          </div>
          <div class="field span2">
            <label>概要</label>
            <input v-model="form.description" placeholder="案件の概要" />
          </div>
          <div class="field">
            <label>必要スキル</label>
            <input v-model="form.required_skill" placeholder="Java, AWS など" />
          </div>
          <div class="field">
            <label>歓迎スキル</label>
            <input v-model="form.preferred_skill" placeholder="Python など" />
          </div>
          <div class="field">
            <label>エンド顧客</label>
            <select v-model="form.end_client_id">
              <option value="">-- 選択 --</option>
              <option v-for="c in clients" :key="c.id" :value="String(c.id)">{{ c.name }}</option>
            </select>
          </div>
          <div class="field">
            <label>プライム</label>
            <select v-model="form.prime_client_id">
              <option value="">-- 選択 --</option>
              <option v-for="c in clients" :key="c.id" :value="String(c.id)">{{ c.name }}</option>
            </select>
          </div>
          <div class="field">
            <label>中間1</label>
            <select v-model="form.mid1_client_id">
              <option value="">-- 選択 --</option>
              <option v-for="c in clients" :key="c.id" :value="String(c.id)">{{ c.name }}</option>
            </select>
          </div>
          <div class="field">
            <label>中間2</label>
            <select v-model="form.mid2_client_id">
              <option value="">-- 選択 --</option>
              <option v-for="c in clients" :key="c.id" :value="String(c.id)">{{ c.name }}</option>
            </select>
          </div>
          <div class="field">
            <label>契約企業</label>
            <select v-model="form.contract_client_id">
              <option value="">-- 選択 --</option>
              <option v-for="c in clients" :key="c.id" :value="String(c.id)">{{ c.name }}</option>
            </select>
          </div>
          <div class="field span3">
            <label>想定工程</label>
            <div class="checkbox-group">
              <label v-for="proc in PROCESSES" :key="proc" class="inline-label">
                <input type="checkbox" :value="proc" v-model="form.process_flags" />
                {{ proc }}
              </label>
            </div>
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
.checkbox-group {
  display: flex;
  flex-wrap: wrap;
  gap: 8px 16px;
  padding: 8px 0 2px;
}
</style>
