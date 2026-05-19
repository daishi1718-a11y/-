export interface Client {
  id: number
  client_code: string
  name: string
  industry: string | null
  size: string | null
  status: string
  note: string | null
}

export interface ClientCreate {
  client_code: string
  name: string
  industry?: string | null
  size?: string | null
  status: string
  note?: string | null
}
