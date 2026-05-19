import axios from 'axios'
import type { Project, ProjectCreate } from '@/types/project'

const api = axios.create({ baseURL: 'http://localhost:8000' })

export const getProjects = (): Promise<Project[]> =>
  api.get<Project[]>('/api/projects').then(r => r.data)

export const getProject = (id: number): Promise<Project> =>
  api.get<Project>(`/api/projects/${id}`).then(r => r.data)

export const createProject = (body: ProjectCreate): Promise<Project> =>
  api.post<Project>('/api/projects', body).then(r => r.data)

export const updateProject = (id: number, body: ProjectCreate): Promise<Project> =>
  api.put<Project>(`/api/projects/${id}`, body).then(r => r.data)

export const deleteProject = (id: number): Promise<void> =>
  api.delete(`/api/projects/${id}`).then(() => undefined)
