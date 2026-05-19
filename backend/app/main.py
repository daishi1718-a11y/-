from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, Base
from .routers import employees, clients, projects, assignments, staffing

Base.metadata.create_all(bind=engine)

app = FastAPI(title="案件・要員管理システム")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(employees.router)
app.include_router(clients.router)
app.include_router(projects.router)
app.include_router(assignments.router)
app.include_router(staffing.router)
