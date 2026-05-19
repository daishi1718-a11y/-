from sqlalchemy.orm import Session
from . import models, schemas


# ── Employee ──────────────────────────────────────────────────
def get_employees(db: Session):
    return db.query(models.Employee).all()


def get_employee(db: Session, employee_id: int):
    return db.query(models.Employee).filter(models.Employee.id == employee_id).first()


def create_employee(db: Session, body: schemas.EmployeeCreate):
    obj = models.Employee(**body.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_employee(db: Session, employee_id: int, body: schemas.EmployeeCreate):
    obj = get_employee(db, employee_id)
    if not obj:
        return None
    for key, value in body.model_dump().items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete_employee(db: Session, employee_id: int):
    obj = get_employee(db, employee_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True


# ── Client ────────────────────────────────────────────────────
def get_clients(db: Session):
    return db.query(models.Client).all()


def get_client(db: Session, client_id: int):
    return db.query(models.Client).filter(models.Client.id == client_id).first()


def create_client(db: Session, body: schemas.ClientCreate):
    obj = models.Client(**body.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_client(db: Session, client_id: int, body: schemas.ClientCreate):
    obj = get_client(db, client_id)
    if not obj:
        return None
    for key, value in body.model_dump().items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete_client(db: Session, client_id: int):
    obj = get_client(db, client_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True


# ── Project ───────────────────────────────────────────────────
def get_projects(db: Session):
    return db.query(models.Project).all()


def get_project(db: Session, project_id: int):
    return db.query(models.Project).filter(models.Project.id == project_id).first()


def create_project(db: Session, body: schemas.ProjectCreate):
    obj = models.Project(**body.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_project(db: Session, project_id: int, body: schemas.ProjectCreate):
    obj = get_project(db, project_id)
    if not obj:
        return None
    for key, value in body.model_dump().items():
        setattr(obj, key, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete_project(db: Session, project_id: int):
    obj = get_project(db, project_id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
