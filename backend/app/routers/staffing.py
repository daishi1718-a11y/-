from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, joinedload
from datetime import date
from calendar import monthrange

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/staffing", tags=["staffing"])


@router.get("/matrix", response_model=schemas.StaffingMatrix)
def get_matrix(
    from_month: str = Query(..., alias="from", description="YYYY-MM"),
    to_month: str = Query(..., alias="to", description="YYYY-MM"),
    db: Session = Depends(get_db),
):
    # 対象月リストを生成
    def month_range(start: str, end: str) -> list[str]:
        months = []
        y, m = int(start[:4]), int(start[5:7])
        ey, em = int(end[:4]), int(end[5:7])
        while (y, m) <= (ey, em):
            months.append(f"{y:04d}-{m:02d}")
            m += 1
            if m > 12:
                m = 1
                y += 1
        return months

    months = month_range(from_month, to_month)

    employees = db.query(models.Employee).filter(models.Employee.status != "退職").all()
    assignments = (
        db.query(models.Assignment)
        .options(joinedload(models.Assignment.project))
        .filter(models.Assignment.status != "完了")
        .all()
    )

    rows = []
    for emp in employees:
        emp_assignments = [a for a in assignments if a.employee_id == emp.id]
        month_cells: dict[str, schemas.StaffingCell] = {}

        for ym in months:
            y, m = int(ym[:4]), int(ym[5:7])
            month_start = date(y, m, 1)
            month_end = date(y, m, monthrange(y, m)[1])

            matched = [
                a for a in emp_assignments
                if a.start_date <= month_end and a.end_date >= month_start
            ]

            if matched:
                a = matched[0]
                month_cells[ym] = schemas.StaffingCell(
                    status=a.status,
                    project_name=a.project.name,
                )
            else:
                month_cells[ym] = schemas.StaffingCell(status="空き")

        rows.append(schemas.StaffingRow(
            employee_id=emp.id,
            employee_name=emp.name,
            months=month_cells,
        ))

    return schemas.StaffingMatrix(months=months, rows=rows)
