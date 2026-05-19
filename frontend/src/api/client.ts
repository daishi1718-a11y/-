import axios, { AxiosError } from 'axios'

export const apiClient = axios.create({ baseURL: 'http://localhost:8000' })

export function extractError(e: unknown): string {
  if (e instanceof AxiosError) {
    const detail = e.response?.data?.detail
    if (typeof detail === 'string') return detail
    if (Array.isArray(detail)) return detail.map((d: { msg?: string }) => d.msg ?? '').join(', ')
    if (e.code === 'ERR_NETWORK') return 'バックエンドに接続できません。サーバーが起動しているか確認してください。'
  }
  return '操作に失敗しました'
}
