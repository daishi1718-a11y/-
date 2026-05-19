import { apiClient as api } from '@/api/client'
import type { Assignment, AssignmentCreate } from '@/types/assignment'


export const getAssignments = (): Promise<Assignment[]> =>
  api.get<Assignment[]>('/api/assignments').then(r => r.data)

export const getAssignment = (id: number): Promise<Assignment> =>
  api.get<Assignment>(`/api/assignments/${id}`).then(r => r.data)

export const createAssignment = (body: AssignmentCreate): Promise<Assignment> =>
  api.post<Assignment>('/api/assignments', body).then(r => r.data)

export const updateAssignment = (id: number, body: AssignmentCreate): Promise<Assignment> =>
  api.put<Assignment>(`/api/assignments/${id}`, body).then(r => r.data)

export const deleteAssignment = (id: number): Promise<void> =>
  api.delete(`/api/assignments/${id}`).then(() => undefined)
