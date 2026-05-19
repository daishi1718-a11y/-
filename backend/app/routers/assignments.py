from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/assignments", tags=["assignments"])


def _to_out(a: models.Assignment) -> schemas.AssignmentOut:
    """ORM object → AssignmentOut（社員名・案件名を付加）"""
    return schemas.AssignmentOut(
        id=a.id,
        employee_id=a.employee_id,
        project_id=a.project_id,
        branch_no=a.branch_no,
        rank=a.rank,
        utilization=a.utilization,
        start_date=a.start_date,
        end_date=a.end_date,
        status=a.status,
        unit_price=a.unit_price,
        note=a.note,
        employee_name=a.employee.name,
        project_name=a.project.name,
    )


def _load(db: Session, assignment_id: int) -> models.Assignment:
    return (
        db.query(models.Assignment)
        .options(
            joinedload(models.Assignment.employee),
            joinedload(models.Assignment.project),
        )
        .filter(models.Assignment.id == assignment_id)
        .first()
    )


@router.get("", response_model=List[schemas.AssignmentOut])
def list_assignments(db: Session = Depends(get_db)):
    assignments = (
        db.query(models.Assignment)
        .options(
            joinedload(models.Assignment.employee),
            joinedload(models.Assignment.project),
        )
        .all()
    )
    return [_to_out(a) for a in assignments]


@router.post("", response_model=schemas.AssignmentOut, status_code=201)
def create_assignment(body: schemas.AssignmentCreate, db: Session = Depends(get_db)):
    employee = db.query(models.Employee).filter(models.Employee.id == body.employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    project = db.query(models.Project).filter(models.Project.id == body.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    a = models.Assignment(**body.model_dump())
    db.add(a)
    db.commit()
    db.refresh(a)
    return _to_out(_load(db, a.id))


@router.get("/{id}", response_model=schemas.AssignmentOut)
def get_assignment(id: int, db: Session = Depends(get_db)):
    a = _load(db, id)
    if not a:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return _to_out(a)


@router.put("/{id}", response_model=schemas.AssignmentOut)
def update_assignment(id: int, body: schemas.AssignmentCreate, db: Session = Depends(get_db)):
    a = _load(db, id)
    if not a:
        raise HTTPException(status_code=404, detail="Assignment not found")

    employee = db.query(models.Employee).filter(models.Employee.id == body.employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    project = db.query(models.Project).filter(models.Project.id == body.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    for key, value in body.model_dump().items():
        setattr(a, key, value)
    db.commit()
    db.refresh(a)
    return _to_out(_load(db, a.id))


@router.delete("/{id}", status_code=204)
def delete_assignment(id: int, db: Session = Depends(get_db)):
    a = db.query(models.Assignment).filter(models.Assignment.id == id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Assignment not found")
    db.delete(a)
    db.commit()
