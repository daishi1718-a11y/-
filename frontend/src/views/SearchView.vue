<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { searchKnowledge } from '@/api/search'
import { getEmployees } from '@/api/employees'
import { getClients } from '@/api/clients'
import type { SearchResult } from '@/types/search'
import type { Employee } from '@/types/employee'
import type { Client } from '@/types/client'

const STATUSES = ['契約期間中', '内諾', '完了']

const employees = ref<Employee[]>([])
const clients = ref<Client[]>([])
const results = ref<SearchResult[]>([])
const searched = ref(false)
const loading = ref(false)
const error = ref('')

const params = reactive({
  q: '',
  employee_id: '',
  client_id: '',
  assignment_status: '',
})

// 展開中の行
const expandedId = ref<number | null>(null)
function toggleExpand(id: number) {
  expandedId.value = expandedId.value === id ? null : id
}

async function load() {
  try {
    const [emp, cli] = await Promise.all([getEmployees(), getClients()])
    employees.value = emp
    clients.value = cli
  } catch {
    error.value = 'マスタデータの取得に失敗しました'
  }
}

async function doSearch() {
  loading.value = true
  error.value = ''
  try {
    results.value = await searchKnowledge({
      q: params.q || undefined,
      employee_id: params.employee_id ? Number(params.employee_id) : undefined,
      client_id: params.client_id ? Number(params.client_id) : undefined,
      assignment_status: params.assignment_status || undefined,
    })
    searched.value = true
    expandedId.value = null
  } catch {
    error.value = '検索に失敗しました'
  } finally {
    loading.value = false
  }
}

function resetParams() {
  params.q = ''
  params.employee_id = ''
  params.client_id = ''
  params.assignment_status = ''
  results.value = []
  searched.value = false
}

function commercialFlow(r: SearchResult): string {
  return [r.end_client_name, r.prime_client_name, r.mid1_client_name, r.mid2_client_name, r.contract_client_name]
    .filter(Boolean)
    .join(' → ')
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
    <h2>ナレッジ検索</h2>
    <p class="desc">誰がどの案件に入っていたか・スキル・商流を横断検索できます</p>

    <div class="search-box">
      <div class="search-row">
        <label class="wide">
          フリーワード
          <input
            v-model="params.q"
            placeholder="社員名・案件名・スキル・メモ など"
            @keyup.enter="doSearch"
          />
        </label>
        <label>
          社員
          <select v-model="params.employee_id">
            <option value="">すべて</option>
            <option v-for="e in employees" :key="e.id" :value="String(e.id)">{{ e.name }}</option>
          </select>
        </label>
        <label>
          顧客
          <select v-model="params.client_id">
            <option value="">すべて</option>
            <option v-for="c in clients" :key="c.id" :value="String(c.id)">{{ c.name }}</option>
          </select>
        </label>
        <label>
          ステータス
          <select v-model="params.assignment_status">
            <option value="">すべて</option>
            <option v-for="s in STATUSES" :key="s" :value="s">{{ s }}</option>
          </select>
        </label>
      </div>
      <div class="search-actions">
        <button class="primary" @click="doSearch" :disabled="loading">
          {{ loading ? '検索中...' : '検索' }}
        </button>
        <button @click="resetParams">クリア</button>
      </div>
    </div>

    <p v-if="error" class="error">{{ error }}</p>

    <div v-if="searched" class="results">
      <div class="result-header">
        検索結果：<strong>{{ results.length }} 件</strong>
      </div>

      <p v-if="results.length === 0" class="no-results">条件に一致するデータがありません</p>

      <table v-else>
        <thead>
          <tr>
            <th></th>
            <th>社員名</th>
            <th>クラス</th>
            <th>案件名</th>
            <th>エンド顧客</th>
            <th>役割</th>
            <th>期間</th>
            <th>ステータス</th>
          </tr>
        </thead>
        <tbody>
          <template v-for="r in results" :key="r.assignment_id">
            <tr class="clickable" @click="toggleExpand(r.assignment_id)">
              <td class="expand-icon">{{ expandedId === r.assignment_id ? '▼' : '▶' }}</td>
              <td><strong>{{ r.employee_name }}</strong></td>
              <td>{{ r.employee_position }}</td>
              <td>{{ r.project_name }}</td>
              <td>{{ r.end_client_name ?? '―' }}</td>
              <td>{{ r.role ?? '―' }}</td>
              <td class="nowrap">{{ r.start_date }} 〜 {{ r.end_date }}</td>
              <td><span :class="statusClass(r.assignment_status)">{{ r.assignment_status }}</span></td>
            </tr>
            <tr v-if="expandedId === r.assignment_id" class="detail-row">
              <td colspan="8">
                <div class="detail">
                  <div class="detail-grid">
                    <div class="detail-section">
                      <h4>社員情報</h4>
                      <dl>
                        <dt>在籍状況</dt><dd>{{ r.employee_status }}</dd>
                        <dt>アサイン時ランク</dt><dd>{{ r.rank ?? '―' }}</dd>
                        <dt>稼働率</dt><dd>{{ r.utilization * 100 }}%</dd>
                        <dt>単価</dt><dd>{{ r.unit_price !== null ? r.unit_price.toLocaleString() + ' 円' : '―' }}</dd>
                      </dl>
                    </div>
                    <div class="detail-section">
                      <h4>案件情報</h4>
                      <dl>
                        <dt>案件コード</dt><dd>{{ r.project_code }}</dd>
                        <dt>概要</dt><dd>{{ r.description ?? '―' }}</dd>
                        <dt>必要スキル</dt><dd>{{ r.required_skill ?? '―' }}</dd>
                        <dt>歓迎スキル</dt><dd>{{ r.preferred_skill ?? '―' }}</dd>
                        <dt>想定工程</dt><dd>{{ r.process_flags ?? '―' }}</dd>
                      </dl>
                    </div>
                    <div class="detail-section">
                      <h4>商流</h4>
                      <div class="flow">{{ commercialFlow(r) || '―' }}</div>
                      <dl>
                        <dt>エンド</dt><dd>{{ r.end_client_name ?? '―' }}</dd>
                        <dt>プライム</dt><dd>{{ r.prime_client_name ?? '―' }}</dd>
                        <dt>中間1</dt><dd>{{ r.mid1_client_name ?? '―' }}</dd>
                        <dt>中間2</dt><dd>{{ r.mid2_client_name ?? '―' }}</dd>
                        <dt>契約</dt><dd>{{ r.contract_client_name ?? '―' }}</dd>
                      </dl>
                    </div>
                    <div v-if="r.note" class="detail-section span2">
                      <h4>メモ</h4>
                      <p>{{ r.note }}</p>
                    </div>
                  </div>
                </div>
              </td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.page { padding: 1.5rem; }
h2 { margin-bottom: 0.25rem; }
.desc { color: #64748b; font-size: 0.85rem; margin-bottom: 1.25rem; }

.search-box {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  padding: 1rem;
  margin-bottom: 1.5rem;
}
.search-row {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 0.75rem;
  margin-bottom: 0.75rem;
}
.wide { grid-column: 1; }
label { display: flex; flex-direction: column; font-size: 0.85rem; gap: 0.25rem; }
input, select { padding: 0.35rem 0.5rem; border: 1px solid #cbd5e1; border-radius: 4px; font-size: 0.9rem; }
.search-actions { display: flex; gap: 0.5rem; }
button { padding: 0.4rem 1.25rem; cursor: pointer; border: 1px solid #94a3b8; background: #fff; border-radius: 4px; font-size: 0.9rem; }
button:hover { background: #f1f5f9; }
button.primary { background: #1e293b; color: #f8fafc; border-color: #1e293b; }
button.primary:hover { background: #334155; }
button:disabled { opacity: 0.5; cursor: not-allowed; }

.result-header { margin-bottom: 0.75rem; font-size: 0.9rem; color: #475569; }

table { border-collapse: collapse; width: 100%; font-size: 0.9rem; }
th, td { border: 1px solid #cbd5e1; padding: 0.4rem 0.6rem; text-align: left; }
th { background: #f1f5f9; white-space: nowrap; }
.clickable { cursor: pointer; }
.clickable:hover { background: #f8fafc; }
.expand-icon { text-align: center; color: #94a3b8; font-size: 0.75rem; width: 1.5rem; }
.nowrap { white-space: nowrap; }

.detail-row td { padding: 0; background: #f8fafc; }
.detail { padding: 1rem; }
.detail-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}
.span2 { grid-column: span 2; }
.detail-section h4 { font-size: 0.8rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem; border-bottom: 1px solid #e2e8f0; padding-bottom: 0.25rem; }
dl { display: grid; grid-template-columns: 6rem 1fr; gap: 0.2rem 0.5rem; font-size: 0.85rem; }
dt { color: #64748b; }
dd { color: #1e293b; }
.flow { font-size: 0.85rem; color: #0f172a; margin-bottom: 0.5rem; font-weight: 500; }

.badge-active { background: #dcfce7; color: #166534; padding: 0.15rem 0.4rem; border-radius: 3px; font-size: 0.8rem; }
.badge-pending { background: #fef9c3; color: #713f12; padding: 0.15rem 0.4rem; border-radius: 3px; font-size: 0.8rem; }
.badge-done { background: #f1f5f9; color: #475569; padding: 0.15rem 0.4rem; border-radius: 3px; font-size: 0.8rem; }
.no-results { color: #94a3b8; padding: 1rem 0; }
.error { color: #dc2626; margin-bottom: 0.75rem; }
</style>
