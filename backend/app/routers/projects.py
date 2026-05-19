from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/projects", tags=["projects"])


def _validate_client_ids(db: Session, body: schemas.ProjectCreate) -> None:
    client_fields = {
        "end_client_id": body.end_client_id,
        "prime_client_id": body.prime_client_id,
        "mid1_client_id": body.mid1_client_id,
        "mid2_client_id": body.mid2_client_id,
        "contract_client_id": body.contract_client_id,
    }
    for field, cid in client_fields.items():
        if cid is not None:
            if not db.query(models.Client).filter(models.Client.id == cid).first():
                raise HTTPException(status_code=404, detail=f"Client not found: {field}={cid}")


@router.get("", response_model=List[schemas.Project])
def list_projects(db: Session = Depends(get_db)):
    return crud.get_projects(db)


@router.post("", response_model=schemas.Project, status_code=201)
def create_project(body: schemas.ProjectCreate, db: Session = Depends(get_db)):
    _validate_client_ids(db, body)
    return crud.create_project(db, body)


@router.get("/{id}", response_model=schemas.Project)
def get_project(id: int, db: Session = Depends(get_db)):
    obj = crud.get_project(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Project not found")
    return obj


@router.put("/{id}", response_model=schemas.Project)
def update_project(id: int, body: schemas.ProjectCreate, db: Session = Depends(get_db)):
    _validate_client_ids(db, body)
    obj = crud.update_project(db, id, body)
    if not obj:
        raise HTTPException(status_code=404, detail="Project not found")
    return obj


@router.delete("/{id}", status_code=204)
def delete_project(id: int, db: Session = Depends(get_db)):
    if not crud.delete_project(db, id):
        raise HTTPException(status_code=404, detail="Project not found")
