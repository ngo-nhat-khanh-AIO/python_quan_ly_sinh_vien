from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import sinh_vien, mon_hoc, ket_qua

app = FastAPI(title="Quản lý Sinh viên API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    sinh_vien.router, prefix="/api/sinh-vien", tags=["sinh-vien"])
app.include_router(mon_hoc.router, prefix="/api/mon-hoc", tags=["mon-hoc"])
app.include_router(ket_qua.router, prefix="/api/ket-qua", tags=["ket_qua"])
