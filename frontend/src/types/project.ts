export interface Project {
  id: number
  project_code: string
  name: string
  description: string | null
  role: string | null
  required_skill: string | null
  preferred_skill: string | null
  process_flags: string | null
  end_client_id: number | null
  prime_client_id: number | null
  mid1_client_id: number | null
  mid2_client_id: number | null
  contract_client_id: number | null
}

export interface ProjectCreate {
  project_code: string
  name: string
  description?: string | null
  role?: string | null
  required_skill?: string | null
  preferred_skill?: string | null
  process_flags?: string | null
  end_client_id?: number | null
  prime_client_id?: number | null
  mid1_client_id?: number | null
  mid2_client_id?: number | null
  contract_client_id?: number | null
}
