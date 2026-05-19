from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from datetime import date
from calendar import monthrange

from .. import models, schemas
from ..database import get_db

_STATUS_PRIORITY = {"契約期間中": 0, "内諾": 1}

router = APIRouter(prefix="/api/staffing", tags=["staffing"])


def _build_months(start: str, end: str) -> list[str]:
    months = []
    y, m = int(start[:4]), int(start[5:7])
    ey, em = int(end[:4]), int(end[5:7])
    while (y, m) <= (ey, em):
        months.append(f"{y:04d}-{m:02d}")
        m += 1
        if m > 12:
            m, y = 1, y + 1
    return months


@router.get("/matrix", response_model=schemas.StaffingMatrix)
def get_matrix(
    from_month: str = Query(..., alias="from", description="YYYY-MM"),
    to_month: str = Query(..., alias="to", description="YYYY-MM"),
    db: Session = Depends(get_db),
):
    if from_month > to_month:
        raise HTTPException(status_code=422, detail="from は to 以前の月を指定してください")
    months = _build_months(from_month, to_month)

    employees = (
        db.query(models.Employee)
        .filter(models.Employee.status != "退職")
        .order_by(models.Employee.employee_code)
        .all()
    )

    # 期間が重なるアサインを一括取得（完了済みを除く）
    from_date = date(int(from_month[:4]), int(from_month[5:7]), 1)
    to_y, to_m = int(to_month[:4]), int(to_month[5:7])
    to_date = date(to_y, to_m, monthrange(to_y, to_m)[1])

    assignments = (
        db.query(models.Assignment)
        .options(joinedload(models.Assignment.project))
        .filter(
            models.Assignment.status != "完了",
            models.Assignment.start_date <= to_date,
            models.Assignment.end_date >= from_date,
        )
        .all()
    )

    # employee_id → assignments のマップを事前構築（N+1回避）
    assign_map: dict[int, list[models.Assignment]] = {}
    for a in assignments:
        assign_map.setdefault(a.employee_id, []).append(a)

    rows = []
    for emp in employees:
        emp_assignments = assign_map.get(emp.id, [])
        cells: dict[str, schemas.StaffingCell] = {}

        for ym in months:
            y, m = int(ym[:4]), int(ym[5:7])
            month_start = date(y, m, 1)
            month_end = date(y, m, monthrange(y, m)[1])

            matched = [
                a for a in emp_assignments
                if a.start_date <= month_end and a.end_date >= month_start
            ]

            if matched:
                if len(matched) == 1:
                    a = matched[0]
                    cells[ym] = schemas.StaffingCell(
                        status=a.status,
                        project_name=a.project.name,
                        count=1,
                    )
                else:
                    best = min(matched, key=lambda a: _STATUS_PRIORITY.get(a.status, 99))
                    cells[ym] = schemas.StaffingCell(
                        status=best.status,
                        project_name=" / ".join(a.project.name for a in matched),
                        count=len(matched),
                    )
            else:
                cells[ym] = schemas.StaffingCell(status="空き", count=0)

        rows.append(schemas.StaffingRow(
            employee_id=emp.id,
            employee_name=emp.name,
            cells=cells,
        ))

    return schemas.StaffingMatrix(months=months, rows=rows)
