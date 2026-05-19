from pydantic import BaseModel, field_validator, model_validator
from typing import Optional
from datetime import date

_POSITIONS = {'アナリスト', 'コンサルタント', 'シニアコンサルタント', 'マネージャー', 'シニアマネージャー', 'ディレクター', 'パートナー'}
_EMP_STATUSES = {'在籍', '退職', '入社見込み'}
_CLI_STATUSES = {'利用', '利用停止'}
_ASN_STATUSES = {'契約期間中', '内諾', '完了'}


# ── Employee ──────────────────────────────────────────────────
class EmployeeBase(BaseModel):
    employee_code: str
    name: str
    position: str
    status: str
    joined_at: Optional[date] = None
    left_at: Optional[date] = None

    @field_validator('employee_code', 'name')
    @classmethod
    def required_str(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('必須項目です')
        return v.strip()

    @field_validator('position')
    @classmethod
    def valid_position(cls, v: str) -> str:
        if v not in _POSITIONS:
            raise ValueError(f'クラスの値が不正です: {v}')
        return v

    @field_validator('status')
    @classmethod
    def valid_status(cls, v: str) -> str:
        if v not in _EMP_STATUSES:
            raise ValueError(f'在籍状況の値が不正です: {v}')
        return v


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

    @field_validator('client_code', 'name')
    @classmethod
    def required_str(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('必須項目です')
        return v.strip()

    @field_validator('status')
    @classmethod
    def valid_status(cls, v: str) -> str:
        if v not in _CLI_STATUSES:
            raise ValueError(f'ステータスの値が不正です: {v}')
        return v


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

    @field_validator('project_code', 'name')
    @classmethod
    def required_str(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('必須項目です')
        return v.strip()


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

    @field_validator('utilization')
    @classmethod
    def valid_utilization(cls, v: float) -> float:
        if not (0 < v <= 1.0):
            raise ValueError('稼働率は 0 より大きく 1.0 以下の値を指定してください')
        return v

    @field_validator('unit_price')
    @classmethod
    def valid_unit_price(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and v < 0:
            raise ValueError('単価は 0 以上の値を指定してください')
        return v

    @field_validator('status')
    @classmethod
    def valid_status(cls, v: str) -> str:
        if v not in _ASN_STATUSES:
            raise ValueError(f'ステータスの値が不正です: {v}')
        return v

    @model_validator(mode='after')
    def date_order(self) -> 'AssignmentBase':
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValueError('開始日は終了日以前の日付を指定してください')
        return self


class AssignmentCreate(AssignmentBase):
    pass


class AssignmentOut(AssignmentBase):
    id: int
    employee_name: str
    project_name: str

    model_config = {"from_attributes": True}


# ── Staffing ──────────────────────────────────────────────────
class StaffingCell(BaseModel):
    status: str                     # "契約期間中" | "内諾" | "空き" | "複数"
    project_name: Optional[str] = None
    count: int = 1                  # number of overlapping assignments


class StaffingRow(BaseModel):
    employee_id: int
    employee_name: str
    cells: dict[str, StaffingCell]  # key: "YYYY-MM"


class StaffingMatrix(BaseModel):
    months: list[str]
    rows: list[StaffingRow]


# ── Search ────────────────────────────────────────────────────
class SearchParams(BaseModel):
    q: Optional[str] = None
    employee_id: Optional[int] = None
    client_id: Optional[int] = None
    assignment_status: Optional[str] = None


class SearchResult(BaseModel):
    assignment_id: int
    employee_id: int
    employee_name: str
    employee_position: str
    employee_status: str
    project_id: int
    project_name: str
    project_code: str
    description: Optional[str]
    required_skill: Optional[str]
    preferred_skill: Optional[str]
    process_flags: Optional[str]
    role: Optional[str]
    branch_no: Optional[int]
    rank: Optional[str]
    utilization: float
    start_date: str
    end_date: str
    assignment_status: str
    unit_price: Optional[int]
    note: Optional[str]
    end_client_name: Optional[str]
    prime_client_name: Optional[str]
    mid1_client_name: Optional[str]
    mid2_client_name: Optional[str]
    contract_client_name: Optional[str]
