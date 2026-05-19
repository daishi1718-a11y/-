<script setup lang="ts">
import { extractError } from '@/api/client'
import { ref, reactive, onMounted } from 'vue'
import { searchKnowledge } from '@/api/search'
import { getEmployees } from '@/api/employees'
import { getClients } from '@/api/clients'
import type { SearchResult } from '@/types/search'
import type { Employee } from '@/types/employee'
import type { Client } from '@/types/client'
import { downloadCsv } from '@/utils/csv'

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
  } catch (e) {
    error.value = extractError(e)
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
  } catch (e) {
    error.value = extractError(e)
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

function exportCsv() {
  const headers = ['社員名', 'クラス', '案件名', 'エンド顧客', '役割', '開始日', '終了日', 'ステータス', '稼働率', '単価', 'メモ']
  const rows = results.value.map(r => [
    r.employee_name,
    r.employee_position,
    r.project_name,
    r.end_client_name ?? '',
    r.role ?? '',
    r.start_date,
    r.end_date,
    r.assignment_status,
    `${Math.round(r.utilization * 100)}%`,
    r.unit_price !== null ? String(r.unit_price) : '',
    r.note ?? '',
  ])
  downloadCsv(headers, rows, 'ナレッジ検索結果.csv')
}

function statusBadgeClass(status: string): string {
  if (status === '契約期間中') return 'badge badge-active'
  if (status === '内諾') return 'badge badge-pending'
  return 'badge badge-done'
}

onMounted(load)
</script>

<template>
  <div class="page">
    <div class="page-header">
      <div>
        <div class="page-title">ナレッジ検索</div>
        <div class="page-desc">誰がどの案件に入っていたか・スキル・商流を横断検索</div>
      </div>
    </div>

    <div v-if="error" class="error-banner">
      <svg viewBox="0 0 20 20" fill="currentColor" style="width:16px;height:16px;flex-shrink:0;margin-top:1px"><path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/></svg>
      {{ error }}
    </div>

    <div class="card" style="margin-bottom:20px">
      <div class="card-body">
        <div class="search-freeword">
          <div class="field">
            <label>フリーワード</label>
            <div class="search-input-wrap">
              <svg class="search-icon" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd"/></svg>
              <input
                v-model="params.q"
                placeholder="社員名・案件名・スキル・メモなど"
                @keyup.enter="doSearch"
                class="search-input"
              />
            </div>
          </div>
        </div>
        <div class="search-filters">
          <div class="field">
            <label>社員</label>
            <select v-model="params.employee_id">
              <option value="">すべて</option>
              <option v-for="e in employees" :key="e.id" :value="String(e.id)">{{ e.name }}</option>
            </select>
          </div>
          <div class="field">
            <label>顧客</label>
            <select v-model="params.client_id">
              <option value="">すべて</option>
              <option v-for="c in clients" :key="c.id" :value="String(c.id)">{{ c.name }}</option>
            </select>
          </div>
          <div class="field">
            <label>ステータス</label>
            <select v-model="params.assignment_status">
              <option value="">すべて</option>
              <option v-for="s in STATUSES" :key="s" :value="s">{{ s }}</option>
            </select>
          </div>
          <div class="search-actions">
            <button class="btn btn-primary" @click="doSearch" :disabled="loading">
              <svg viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd"/></svg>
              {{ loading ? '検索中...' : '検索' }}
            </button>
            <button class="btn btn-secondary" @click="resetParams">クリア</button>
          </div>
        </div>
      </div>
    </div>

    <div v-if="searched">
      <div class="results-header">
        <span>
          検索結果
          <span class="count-badge">{{ results.length }} 件</span>
        </span>
        <button v-if="results.length > 0" class="btn btn-secondary btn-sm" @click="exportCsv">
          <svg viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clip-rule="evenodd"/></svg>
          CSV出力
        </button>
      </div>

      <div v-if="results.length === 0" class="card">
        <div class="empty-state">条件に一致するデータがありません</div>
      </div>

      <div v-else class="card" style="overflow:hidden">
        <table class="data-table">
          <thead>
            <tr>
              <th style="width:32px"></th>
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
              <tr class="row-clickable" @click="toggleExpand(r.assignment_id)">
                <td style="text-align:center;color:var(--text-3)">
                  <svg v-if="expandedId === r.assignment_id" viewBox="0 0 20 20" fill="currentColor" style="width:12px;height:12px"><path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd"/></svg>
                  <svg v-else viewBox="0 0 20 20" fill="currentColor" style="width:12px;height:12px"><path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd"/></svg>
                </td>
                <td style="font-weight:600">{{ r.employee_name }}</td>
                <td>{{ r.employee_position }}</td>
                <td>{{ r.project_name }}</td>
                <td>{{ r.end_client_name ?? '―' }}</td>
                <td>{{ r.role ?? '―' }}</td>
                <td class="nowrap">{{ r.start_date }} 〜 {{ r.end_date }}</td>
                <td><span :class="statusBadgeClass(r.assignment_status)">{{ r.assignment_status }}</span></td>
              </tr>
              <tr v-if="expandedId === r.assignment_id" class="row-detail">
                <td colspan="8">
                  <div class="detail-panel">
                    <div class="detail-grid">
                      <div class="detail-section">
                        <div class="detail-section-title">社員情報</div>
                        <dl class="detail-dl">
                          <dt>在籍状況</dt><dd>{{ r.employee_status }}</dd>
                          <dt>アサイン時ランク</dt><dd>{{ r.rank ?? '―' }}</dd>
                          <dt>稼働率</dt><dd>{{ Math.round(r.utilization * 100) }}%</dd>
                          <dt>単価</dt><dd>{{ r.unit_price !== null ? r.unit_price.toLocaleString() + ' 円' : '―' }}</dd>
                        </dl>
                      </div>
                      <div class="detail-section">
                        <div class="detail-section-title">案件情報</div>
                        <dl class="detail-dl">
                          <dt>案件コード</dt><dd>{{ r.project_code }}</dd>
                          <dt>概要</dt><dd>{{ r.description ?? '―' }}</dd>
                          <dt>必要スキル</dt><dd>{{ r.required_skill ?? '―' }}</dd>
                          <dt>歓迎スキル</dt><dd>{{ r.preferred_skill ?? '―' }}</dd>
                          <dt>想定工程</dt><dd>{{ r.process_flags ?? '―' }}</dd>
                        </dl>
                      </div>
                      <div class="detail-section">
                        <div class="detail-section-title">商流</div>
                        <div class="flow-line">{{ commercialFlow(r) || '―' }}</div>
                        <dl class="detail-dl">
                          <dt>エンド</dt><dd>{{ r.end_client_name ?? '―' }}</dd>
                          <dt>プライム</dt><dd>{{ r.prime_client_name ?? '―' }}</dd>
                          <dt>中間1</dt><dd>{{ r.mid1_client_name ?? '―' }}</dd>
                          <dt>中間2</dt><dd>{{ r.mid2_client_name ?? '―' }}</dd>
                          <dt>契約</dt><dd>{{ r.contract_client_name ?? '―' }}</dd>
                        </dl>
                      </div>
                      <div v-if="r.note" class="detail-section span2">
                        <div class="detail-section-title">メモ</div>
                        <p style="font-size:13px;color:var(--text)">{{ r.note }}</p>
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
  </div>
</template>

<style scoped>
.search-freeword {
  margin-bottom: 12px;
}
.search-input-wrap {
  position: relative;
  display: flex;
  align-items: center;
}
.search-icon {
  position: absolute;
  left: 10px;
  width: 15px;
  height: 15px;
  color: var(--text-3);
  pointer-events: none;
}
.search-input {
  padding: 8px 10px 8px 34px !important;
}
.search-filters {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr auto;
  gap: 12px;
  align-items: end;
}
.search-actions {
  display: flex;
  gap: 8px;
}

.results-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 13px;
  font-weight: 600;
  color: var(--text-2);
  margin-bottom: 12px;
}

.nowrap { white-space: nowrap; }

.detail-panel {
  padding: 20px;
  background: #f8fafc;
}
.detail-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}
.detail-section {}
.detail-section-title {
  font-size: 10px;
  font-weight: 700;
  color: var(--text-3);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-bottom: 8px;
  padding-bottom: 6px;
  border-bottom: 1px solid var(--border);
}
.detail-dl {
  display: grid;
  grid-template-columns: 7rem 1fr;
  gap: 3px 8px;
  font-size: 12px;
}
.detail-dl dt { color: var(--text-3); }
.detail-dl dd { color: var(--text); }

.flow-line {
  font-size: 12px;
  color: var(--text);
  font-weight: 500;
  margin-bottom: 8px;
  padding: 6px 8px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
}

.span2 { grid-column: span 2; }
</style>
