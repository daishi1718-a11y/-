from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional
from datetime import date

from .. import models
from ..database import get_db
from pydantic import BaseModel

router = APIRouter(prefix="/api/search", tags=["search"])


class SearchResult(BaseModel):
    assignment_id: int
    start_date: date
    end_date: date
    assignment_status: str
    rank: Optional[str]
    utilization: float
    unit_price: Optional[int]
    note: Optional[str]
    # 社員
    employee_id: int
    employee_name: str
    employee_position: str
    employee_status: str
    # 案件
    project_id: int
    project_code: str
    project_name: str
    role: Optional[str]
    required_skill: Optional[str]
    preferred_skill: Optional[str]
    process_flags: Optional[str]
    description: Optional[str]
    # 商流（名前解決済み）
    end_client_name: Optional[str]
    prime_client_name: Optional[str]
    mid1_client_name: Optional[str]
    mid2_client_name: Optional[str]
    contract_client_name: Optional[str]


@router.get("", response_model=list[SearchResult])
def search(
    q: Optional[str] = Query(None, description="フリーワード（社員名・案件名・スキル・メモ）"),
    employee_id: Optional[int] = Query(None, description="社員で絞り込み"),
    client_id: Optional[int] = Query(None, description="顧客で絞り込み（商流のいずれかに一致）"),
    assignment_status: Optional[str] = Query(None, description="アサインステータスで絞り込み"),
    db: Session = Depends(get_db),
):
    query = (
        db.query(models.Assignment)
        .join(models.Employee, models.Assignment.employee_id == models.Employee.id)
        .join(models.Project, models.Assignment.project_id == models.Project.id)
    )

    if employee_id is not None:
        query = query.filter(models.Assignment.employee_id == employee_id)

    if assignment_status:
        query = query.filter(models.Assignment.status == assignment_status)

    if client_id is not None:
        query = query.filter(
            or_(
                models.Project.end_client_id == client_id,
                models.Project.prime_client_id == client_id,
                models.Project.mid1_client_id == client_id,
                models.Project.mid2_client_id == client_id,
                models.Project.contract_client_id == client_id,
            )
        )

    if q:
        kw = f"%{q}%"
        query = query.filter(
            or_(
                models.Employee.name.ilike(kw),
                models.Project.name.ilike(kw),
                models.Project.project_code.ilike(kw),
                models.Project.required_skill.ilike(kw),
                models.Project.preferred_skill.ilike(kw),
                models.Project.description.ilike(kw),
                models.Assignment.note.ilike(kw),
                models.Assignment.rank.ilike(kw),
            )
        )

    rows = query.order_by(
        models.Assignment.employee_id,
        models.Assignment.start_date.desc(),
    ).all()

    # 商流FKを一括取得（N+1回避）
    client_ids: set[int] = set()
    for a in rows:
        prj = a.project
        for cid in [prj.end_client_id, prj.prime_client_id,
                    prj.mid1_client_id, prj.mid2_client_id, prj.contract_client_id]:
            if cid is not None:
                client_ids.add(cid)
    client_map: dict[int, str] = {}
    if client_ids:
        for c in db.query(models.Client).filter(models.Client.id.in_(client_ids)).all():
            client_map[c.id] = c.name

    def cn(cid: Optional[int]) -> Optional[str]:
        return client_map.get(cid) if cid is not None else None

    results = []
    for a in rows:
        emp: models.Employee = a.employee
        prj: models.Project = a.project
        results.append(SearchResult(
            assignment_id=a.id,
            start_date=a.start_date,
            end_date=a.end_date,
            assignment_status=a.status,
            rank=a.rank,
            utilization=a.utilization,
            unit_price=a.unit_price,
            note=a.note,
            employee_id=emp.id,
            employee_name=emp.name,
            employee_position=emp.position,
            employee_status=emp.status,
            project_id=prj.id,
            project_code=prj.project_code,
            project_name=prj.name,
            role=prj.role,
            required_skill=prj.required_skill,
            preferred_skill=prj.preferred_skill,
            process_flags=prj.process_flags,
            description=prj.description,
            end_client_name=cn(prj.end_client_id),
            prime_client_name=cn(prj.prime_client_id),
            mid1_client_name=cn(prj.mid1_client_id),
            mid2_client_name=cn(prj.mid2_client_id),
            contract_client_name=cn(prj.contract_client_id),
        ))
    return results
