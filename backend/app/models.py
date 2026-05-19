from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Index
from sqlalchemy.orm import relationship
from .database import Base


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    employee_code = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    position = Column(String, nullable=False)
    status = Column(String, nullable=False)
    joined_at = Column(Date, nullable=True)
    left_at = Column(Date, nullable=True)

    assignments = relationship("Assignment", back_populates="employee", cascade="all, delete")


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    client_code = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    industry = Column(String, nullable=True)
    size = Column(String, nullable=True)
    status = Column(String, nullable=False)
    note = Column(String, nullable=True)


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    project_code = Column(String, nullable=False, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    role = Column(String, nullable=True)
    required_skill = Column(String, nullable=True)
    preferred_skill = Column(String, nullable=True)
    process_flags = Column(String, nullable=True)
    end_client_id = Column(Integer, ForeignKey("clients.id"), nullable=True, index=True)
    prime_client_id = Column(Integer, ForeignKey("clients.id"), nullable=True)
    mid1_client_id = Column(Integer, ForeignKey("clients.id"), nullable=True)
    mid2_client_id = Column(Integer, ForeignKey("clients.id"), nullable=True)
    contract_client_id = Column(Integer, ForeignKey("clients.id"), nullable=True)

    assignments = relationship("Assignment", back_populates="project", cascade="all, delete")
    end_client = relationship("Client", foreign_keys=[end_client_id])
    prime_client = relationship("Client", foreign_keys=[prime_client_id])
    mid1_client = relationship("Client", foreign_keys=[mid1_client_id])
    mid2_client = relationship("Client", foreign_keys=[mid2_client_id])
    contract_client = relationship("Client", foreign_keys=[contract_client_id])


class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id", ondelete="CASCADE"), nullable=False, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    branch_no = Column(Integer, nullable=True)
    rank = Column(String, nullable=True)
    utilization = Column(Float, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    status = Column(String, nullable=False)
    unit_price = Column(Integer, nullable=True)
    note = Column(String, nullable=True)

    employee = relationship("Employee", back_populates="assignments")
    project = relationship("Project", back_populates="assignments")

    __table_args__ = (
        Index("ix_assignments_dates", "start_date", "end_date"),
    )
