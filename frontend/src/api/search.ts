import { apiClient as api } from '@/api/client'
import type { SearchResult, SearchParams } from '@/types/search'


export const searchKnowledge = (params: SearchParams): Promise<SearchResult[]> =>
  api.get<SearchResult[]>('/api/search', { params }).then(r => r.data)
