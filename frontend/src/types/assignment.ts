export interface Assignment {
  id: number
  employee_id: number
  project_id: number
  branch_no: number | null
  rank: string | null
  utilization: number
  start_date: string
  end_date: string
  status: string
  unit_price: number | null
  note: string | null
  employee_name: string
  project_name: string
}

export interface AssignmentCreate {
  employee_id: number
  project_id: number
  branch_no?: number | null
  rank?: string | null
  utilization: number
  start_date: string
  end_date: string
  status: string
  unit_price?: number | null
  note?: string | null
}
