export interface Employee {
  id: number
  employee_code: string
  name: string
  position: string
  status: string
  joined_at: string | null
  left_at: string | null
}

export interface EmployeeCreate {
  employee_code: string
  name: string
  position: string
  status: string
  joined_at?: string | null
  left_at?: string | null
}
