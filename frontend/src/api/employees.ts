import { apiClient as api } from '@/api/client'
import type { Employee, EmployeeCreate } from '@/types/employee'


export const getEmployees = (): Promise<Employee[]> =>
  api.get<Employee[]>('/api/employees').then(r => r.data)

export const getEmployee = (id: number): Promise<Employee> =>
  api.get<Employee>(`/api/employees/${id}`).then(r => r.data)

export const createEmployee = (body: EmployeeCreate): Promise<Employee> =>
  api.post<Employee>('/api/employees', body).then(r => r.data)

export const updateEmployee = (id: number, body: EmployeeCreate): Promise<Employee> =>
  api.put<Employee>(`/api/employees/${id}`, body).then(r => r.data)

export const deleteEmployee = (id: number): Promise<void> =>
  api.delete(`/api/employees/${id}`).then(() => undefined)
