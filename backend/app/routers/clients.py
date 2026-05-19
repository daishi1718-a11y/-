from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/api/clients", tags=["clients"])


@router.get("", response_model=List[schemas.Client])
def list_clients(db: Session = Depends(get_db)):
    return crud.get_clients(db)


@router.post("", response_model=schemas.Client, status_code=201)
def create_client(body: schemas.ClientCreate, db: Session = Depends(get_db)):
    return crud.create_client(db, body)


@router.get("/{id}", response_model=schemas.Client)
def get_client(id: int, db: Session = Depends(get_db)):
    obj = crud.get_client(db, id)
    if not obj:
        raise HTTPException(status_code=404, detail="Client not found")
    return obj


@router.put("/{id}", response_model=schemas.Client)
def update_client(id: int, body: schemas.ClientCreate, db: Session = Depends(get_db)):
    obj = crud.update_client(db, id, body)
    if not obj:
        raise HTTPException(status_code=404, detail="Client not found")
    return obj


@router.delete("/{id}", status_code=204)
def delete_client(id: int, db: Session = Depends(get_db)):
    if not crud.delete_client(db, id):
        raise HTTPException(status_code=404, detail="Client not found")
