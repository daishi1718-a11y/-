<script setup lang="ts">
import { extractError } from '@/api/client'
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
  } catch (e) {
    error.value = extractError(e)
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
  } catch (e) {
    error.value = extractError(e)
  }
}

async function remove() {
  if (editingId.value === null) return
  if (!confirm('削除しますか？')) return
  try {
    await deleteClient(editingId.value)
    await load()
    resetForm()
  } catch (e) {
    error.value = extractError(e)
  }
}

function statusBadgeClass(status: string): string {
  if (status === '利用') return 'badge badge-active'
  return 'badge badge-done'
}

onMounted(load)
</script>

<template>
  <div class="page">
    <div class="page-header">
      <div>
        <div class="page-title">
          顧客管理
          <span class="count-badge">{{ clients.length }}</span>
        </div>
        <div class="page-desc">顧客マスタの登録・編集</div>
      </div>
      <button class="btn btn-primary" @click="resetForm">
        <svg viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd"/></svg>
        顧客を追加
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
            <th>顧客コード</th>
            <th>顧客名</th>
            <th>業種</th>
            <th>従業員規模</th>
            <th>ステータス</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="c in clients"
            :key="c.id"
            class="row-clickable"
            :class="{ 'row-selected': editingId === c.id }"
            @click="selectRow(c)"
          >
            <td class="text-mono">{{ c.client_code }}</td>
            <td style="font-weight:500">{{ c.name }}</td>
            <td>{{ c.industry ?? '' }}</td>
            <td>{{ c.size ?? '' }}</td>
            <td><span :class="statusBadgeClass(c.status)">{{ c.status }}</span></td>
          </tr>
          <tr v-if="clients.length === 0">
            <td colspan="5" class="empty-state">顧客が登録されていません</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="card">
      <div class="card-header">
        <span class="card-title">{{ editingId !== null ? '顧客を編集' : '新規登録' }}</span>
        <button v-if="editingId !== null" class="btn btn-ghost btn-sm" @click="resetForm">キャンセル</button>
      </div>
      <div class="card-body">
        <div class="form-grid">
          <div class="field">
            <label>顧客コード<span class="req">*</span></label>
            <input v-model="form.client_code" placeholder="CLI001" />
          </div>
          <div class="field span2">
            <label>顧客名<span class="req">*</span></label>
            <input v-model="form.name" placeholder="株式会社〇〇" />
          </div>
          <div class="field">
            <label>業種</label>
            <select v-model="form.industry">
              <option value="">-- 選択 --</option>
              <option v-for="i in INDUSTRIES" :key="i" :value="i">{{ i }}</option>
            </select>
          </div>
          <div class="field">
            <label>従業員規模</label>
            <select v-model="form.size">
              <option value="">-- 選択 --</option>
              <option v-for="s in SIZES" :key="s" :value="s">{{ s }}</option>
            </select>
          </div>
          <div class="field">
            <label>ステータス<span class="req">*</span></label>
            <select v-model="form.status">
              <option value="">-- 選択 --</option>
              <option v-for="s in STATUSES" :key="s" :value="s">{{ s }}</option>
            </select>
          </div>
          <div class="field span3">
            <label>備考</label>
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
</style>
