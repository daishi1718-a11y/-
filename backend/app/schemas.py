from pydantic import BaseModel
from typing import Optional
from datetime import date


# ── Employee ──────────────────────────────────────────────────
class EmployeeBase(BaseModel):
    employee_code: str
    name: str
    position: str
    status: str
    joined_at: Optional[date] = None
    left_at: Optional[date] = None


class EmployeeCreate(EmployeeBase):
    pass


class Employee(EmployeeBase):
    id: int

    model_config = {"from_attributes": True}


# ── Client ────────────────────────────────────────────────────
class ClientBase(BaseModel):
    client_code: str
    name: str
    industry: Optional[str] = None
    size: Optional[str] = None
    status: str
    note: Optional[str] = None


class ClientCreate(ClientBase):
    pass


class Client(ClientBase):
    id: int

    model_config = {"from_attributes": True}


# ── Project ───────────────────────────────────────────────────
class ProjectBase(BaseModel):
    project_code: str
    name: str
    description: Optional[str] = None
    role: Optional[str] = None
    required_skill: Optional[str] = None
    preferred_skill: Optional[str] = None
    process_flags: Optional[str] = None
    end_client_id: Optional[int] = None
    prime_client_id: Optional[int] = None
    mid1_client_id: Optional[int] = None
    mid2_client_id: Optional[int] = None
    contract_client_id: Optional[int] = None


class ProjectCreate(ProjectBase):
    pass


class Project(ProjectBase):
    id: int

    model_config = {"from_attributes": True}


# ── Assignment ────────────────────────────────────────────────
class AssignmentBase(BaseModel):
    employee_id: int
    project_id: int
    branch_no: Optional[int] = None
    rank: Optional[str] = None
    utilization: float
    start_date: date
    end_date: date
    status: str
    unit_price: Optional[int] = None
    note: Optional[str] = None


class AssignmentCreate(AssignmentBase):
    pass


class AssignmentOut(AssignmentBase):
    id: int
    employee_name: str
    project_name: str

    model_config = {"from_attributes": True}


# ── Staffing ──────────────────────────────────────────────────
class StaffingCell(BaseModel):
    status: str          # "契約期間中" | "内諾" | "空き"
    project_name: Optional[str] = None


class StaffingRow(BaseModel):
    employee_id: int
    employee_name: str
    months: dict[str, StaffingCell]  # key: "YYYY-MM"


class StaffingMatrix(BaseModel):
    months: list[str]
    rows: list[StaffingRow]
