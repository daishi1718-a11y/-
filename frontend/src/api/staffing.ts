import { apiClient as api } from '@/api/client'
import type { StaffingMatrix } from '@/types/staffing'


export const getStaffingMatrix = (from: string, to: string): Promise<StaffingMatrix> =>
  api.get<StaffingMatrix>('/api/staffing/matrix', { params: { from, to } }).then(r => r.data)
