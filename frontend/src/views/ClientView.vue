<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { getClients, createClient, updateClient, deleteClient } from '@/api/clients'
import type { Client, ClientCreate } from '@/types/client'

const INDUSTRIES = ['IT/Sier', 'コンサル', '金融（銀行）', '金融（証券）', '金融（保険）', '製造', '運輸', 'ソフトウェア', '通信', '官公庁・独法', '素材・化学', 'ヘルスケア', '建設業', 'インフラ', '不動産', 'サービス・教育', '小売', 'その他']
const SIZES = ['1〜20', '21〜50', '51〜300', '301〜1000', '1001〜']
const STATUSES = ['利用', '利用停止']

const clients = ref<Client[]>([])
const editingId = ref<number | null>(null)
const error = ref('')

const form = reactive({
  client_code: '',
  name: '',
  industry: '',
  size: '',
  status: '',
  note: '',
})

function resetForm() {
  editingId.value = null
  form.client_code = ''
  form.name = ''
  form.industry = ''
  form.size = ''
  form.status = ''
  form.note = ''
}

function selectRow(c: Client) {
  editingId.value = c.id
  form.client_code = c.client_code
  form.name = c.name
  form.industry = c.industry ?? ''
  form.size = c.size ?? ''
  form.status = c.status
  form.note = c.note ?? ''
}

async function load() {
  try {
    clients.value = await getClients()
  } catch {
    error.value = '顧客一覧の取得に失敗しました'
  }
}

async function submit() {
  if (!form.client_code || !form.name || !form.status) {
    error.value = '必須項目を入力してください'
    return
  }
  error.value = ''
  const body: ClientCreate = {
    client_code: form.client_code,
    name: form.name,
    industry: form.industry || null,
    size: form.size || null,
    status: form.status,
    note: form.note || null,
  }
  try {
    if (editingId.value !== null) {
      await updateClient(editingId.value, body)
    } else {
      await createClient(body)
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
    await deleteClient(editingId.value)
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
    <h2>顧客管理</h2>
    <p v-if="error" class="error">{{ error }}</p>

    <table>
      <thead>
        <tr>
          <th>顧客コード</th><th>顧客名</th><th>業種</th><th>従業員規模</th><th>ステータス</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="c in clients"
          :key="c.id"
          :class="{ selected: editingId === c.id }"
          class="clickable"
          @click="selectRow(c)"
        >
          <td>{{ c.client_code }}</td>
          <td>{{ c.name }}</td>
          <td>{{ c.industry ?? '' }}</td>
          <td>{{ c.size ?? '' }}</td>
          <td>{{ c.status }}</td>
        </tr>
      </tbody>
    </table>

    <div class="form-section">
      <h3>{{ editingId !== null ? '編集' : '新規登録' }}</h3>
      <div class="form-grid">
        <label>顧客コード <span class="req">*</span>
          <input v-model="form.client_code" />
        </label>
        <label>顧客名 <span class="req">*</span>
          <input v-model="form.name" />
        </label>
        <label>業種
          <select v-model="form.industry">
            <option value="">-- 選択 --</option>
            <option v-for="i in INDUSTRIES" :key="i" :value="i">{{ i }}</option>
          </select>
        </label>
        <label>従業員規模
          <select v-model="form.size">
            <option value="">-- 選択 --</option>
            <option v-for="s in SIZES" :key="s" :value="s">{{ s }}</option>
          </select>
        </label>
        <label>ステータス <span class="req">*</span>
          <select v-model="form.status">
            <option value="">-- 選択 --</option>
            <option v-for="s in STATUSES" :key="s" :value="s">{{ s }}</option>
          </select>
        </label>
        <label>備考
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
