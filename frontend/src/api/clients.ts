import { apiClient as api } from '@/api/client'
import type { Client, ClientCreate } from '@/types/client'


export const getClients = (): Promise<Client[]> =>
  api.get<Client[]>('/api/clients').then(r => r.data)

export const getClient = (id: number): Promise<Client> =>
  api.get<Client>(`/api/clients/${id}`).then(r => r.data)

export const createClient = (body: ClientCreate): Promise<Client> =>
  api.post<Client>('/api/clients', body).then(r => r.data)

export const updateClient = (id: number, body: ClientCreate): Promise<Client> =>
  api.put<Client>(`/api/clients/${id}`, body).then(r => r.data)

export const deleteClient = (id: number): Promise<void> =>
  api.delete(`/api/clients/${id}`).then(() => undefined)
