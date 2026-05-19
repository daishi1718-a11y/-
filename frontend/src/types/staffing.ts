export interface StaffingCell {
  status: string        // "契約期間中" | "内諾" | "空き"
  project_name: string | null
}

export interface StaffingRow {
  employee_id: number
  employee_name: string
  cells: Record<string, StaffingCell>  // key: "YYYY-MM"
}

export interface StaffingMatrix {
  months: string[]
  rows: StaffingRow[]
}
