from fastapi import APIRouter, HTTPException
from typing import List
from app.models import MonHocBase
import json
from pathlib import Path

router = APIRouter()

DATA_DIR = Path(__file__).parent.parent.parent.parent / "data"


def load_mon_hoc():
    with open(DATA_DIR / "mon_hoc.json", "r", encoding="utf-8") as f:
        return json.load(f)


def save_mon_hoc(data):
    with open(DATA_DIR / "mon_hoc.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# Thay thế mon_hoc_db bằng dữ liệu từ file
mon_hoc_db = load_mon_hoc()


@router.get("/", response_model=List[MonHocBase])
async def get_mon_hoc():
    return mon_hoc_db


@router.post("/", response_model=MonHocBase)
async def create_mon_hoc(mon_hoc: MonHocBase):
    mon_hoc_dict = mon_hoc.dict()
    mon_hoc_db.append(mon_hoc_dict)
    save_mon_hoc(mon_hoc_db)
    return mon_hoc_dict


@router.get("/{ma_mon_hoc}", response_model=MonHocBase)
async def get_mon_hoc_by_ma(ma_mon_hoc: str):
    for mh in mon_hoc_db:
        if mh["ma_mon_hoc"] == ma_mon_hoc:
            return mh
    raise HTTPException(status_code=404, detail="Môn học không tồn tại")
