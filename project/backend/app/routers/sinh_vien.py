import json
from pathlib import Path
from fastapi import APIRouter, HTTPException
from typing import List
from app.models import SinhVienBase

router = APIRouter()

DATA_DIR = Path(__file__).parent.parent.parent.parent / "data"


def load_sinh_vien():
    with open(DATA_DIR / "sinh_vien.json", "r", encoding="utf-8") as f:
        return json.load(f)


def save_sinh_vien(data):
    with open(DATA_DIR / "sinh_vien.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# Thay thế sinh_vien_db bằng dữ liệu từ file
sinh_vien_db = load_sinh_vien()


@router.get("/", response_model=List[SinhVienBase])
async def get_sinh_vien():
    return sinh_vien_db


@router.post("/", response_model=SinhVienBase)
async def create_sinh_vien(sinh_vien: SinhVienBase):
    # Kiểm tra MSSV đã tồn tại chưa
    for sv in sinh_vien_db:
        if sv["mssv"] == sinh_vien.mssv:
            raise HTTPException(
                status_code=400,
                detail="MSSV đã tồn tại"
            )

    # Thêm sinh viên mới
    sinh_vien_dict = sinh_vien.dict()
    sinh_vien_db.append(sinh_vien_dict)

    # Lưu vào file JSON
    save_sinh_vien(sinh_vien_db)

    return sinh_vien_dict


@router.get("/{mssv}", response_model=SinhVienBase)
async def get_sinh_vien_by_mssv(mssv: str):
    for sv in sinh_vien_db:
        if sv["mssv"] == mssv:
            return sv
    raise HTTPException(status_code=404, detail="Sinh viên không tồn tại")


@router.put("/{mssv}", response_model=SinhVienBase)
async def update_sinh_vien(mssv: str, sinh_vien: SinhVienBase):
    for i, sv in enumerate(sinh_vien_db):
        if sv["mssv"] == mssv:
            sinh_vien_db[i] = sinh_vien.dict()
            save_sinh_vien(sinh_vien_db)
            return sinh_vien_db[i]
    raise HTTPException(status_code=404, detail="Sinh viên không tồn tại")


@router.delete("/{mssv}")
async def delete_sinh_vien(mssv: str):
    for i, sv in enumerate(sinh_vien_db):
        if sv["mssv"] == mssv:
            sinh_vien_db.pop(i)
            return {"message": "Đã xóa sinh viên thành công"}
    raise HTTPException(status_code=404, detail="Sinh viên không tồn tại")
