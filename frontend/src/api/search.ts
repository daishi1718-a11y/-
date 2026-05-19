import axios from 'axios'
import type { SearchResult, SearchParams } from '@/types/search'

const api = axios.create({ baseURL: 'http://localhost:8000' })

export const searchKnowledge = (params: SearchParams): Promise<SearchResult[]> =>
  api.get<SearchResult[]>('/api/search', { params }).then(r => r.data)
