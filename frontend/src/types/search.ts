export interface SearchResult {
  assignment_id: number
  start_date: string
  end_date: string
  assignment_status: string
  rank: string | null
  utilization: number
  unit_price: number | null
  note: string | null
  // 社員
  employee_id: number
  employee_name: string
  employee_position: string
  employee_status: string
  // 案件
  project_id: number
  project_code: string
  project_name: string
  role: string | null
  required_skill: string | null
  preferred_skill: string | null
  process_flags: string | null
  description: string | null
  // 商流
  end_client_name: string | null
  prime_client_name: string | null
  mid1_client_name: string | null
  mid2_client_name: string | null
  contract_client_name: string | null
}

export interface SearchParams {
  q?: string
  employee_id?: number
  client_id?: number
  assignment_status?: string
}
