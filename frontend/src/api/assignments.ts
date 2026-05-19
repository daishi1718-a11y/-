import axios from 'axios'
import type { Assignment, AssignmentCreate } from '@/types/assignment'

const api = axios.create({ baseURL: 'http://localhost:8000' })

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
