import axios from 'axios'
import type { StaffingMatrix } from '@/types/staffing'

const api = axios.create({ baseURL: 'http://localhost:8000' })

export const getStaffingMatrix = (from: string, to: string): Promise<StaffingMatrix> =>
  api.get<StaffingMatrix>('/api/staffing/matrix', { params: { from, to } }).then(r => r.data)
