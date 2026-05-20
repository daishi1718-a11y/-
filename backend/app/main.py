from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from .database import engine, Base
from .routers import employees, clients, projects, assignments, staffing, search

Base.metadata.create_all(bind=engine)

app = FastAPI(title="案件・要員管理システム")


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError) -> JSONResponse:
    msg = str(exc.orig) if exc.orig else str(exc)
    if "UNIQUE constraint failed" in msg:
        field = msg.split(".")[-1] if "." in msg else "フィールド"
        detail = f"同じコードがすでに登録されています（{field}）"
    else:
        detail = "データの整合性エラーが発生しました"
    return JSONResponse(status_code=409, content={"detail": detail})

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(employees.router)
app.include_router(clients.router)
app.include_router(projects.router)
app.include_router(assignments.router)
app.include_router(staffing.router)
app.include_router(search.router)
