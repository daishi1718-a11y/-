from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/api/employees", tags=["employees"])


@router.get("", response_model=List[schemas.Employee])
def list_employees(db: Session = Depends(get_db)):
    return crud.get_employees(db)


@router.post("", response_model=schemas.Employee, status_code=201)
def create_employee(body: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    return crud.create_employee(db, body)


@router.get("/{id}", response_model=schemas.Employee)
def get_employee(id: int, db: Session = Depends(get_db)):
    obj = crud.get_employee(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Employee not found")
    return obj


@router.put("/{id}", response_model=schemas.Employee)
def update_employee(id: int, body: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    obj = crud.update_employee(db, id, body)
    if not obj:
        raise HTTPException(status_code=404, detail="Employee not found")
    return obj


@router.delete("/{id}", status_code=204)
def delete_employee(id: int, db: Session = Depends(get_db)):
    if not crud.delete_employee(db, id):
        raise HTTPException(status_code=404, detail="Employee not found")
