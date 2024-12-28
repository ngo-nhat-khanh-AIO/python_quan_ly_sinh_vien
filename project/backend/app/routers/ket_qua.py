from fastapi import APIRouter, HTTPException
from typing import List
from app.models import KetQuaHocTap
import json
from pathlib import Path

router = APIRouter()

DATA_DIR = Path(__file__).parent.parent.parent.parent / "data"


def load_ket_qua():
    with open(DATA_DIR / "ket_qua.json", "r", encoding="utf-8") as f:
        return json.load(f)


def load_mon_hoc():
    with open(DATA_DIR / "mon_hoc.json", "r", encoding="utf-8") as f:
        return json.load(f)


def save_ket_qua(data):
    with open(DATA_DIR / "ket_qua.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# Thay thế ket_qua_db và mon_hoc_db bằng dữ liệu từ file
ket_qua_db = load_ket_qua()
mon_hoc_db = load_mon_hoc()


@router.get("/sinh-vien/{mssv}", response_model=List[KetQuaHocTap])
async def get_ket_qua_by_mssv(mssv: str):
    # Lấy dữ liệu từ file
    ket_qua_db = load_ket_qua()
    mon_hoc_db = load_mon_hoc()  # Thêm dòng này

    results = []
    for kq in ket_qua_db:
        if kq["mssv"] == mssv:
            # Tìm thông tin môn học
            mon_hoc = next(
                (mh for mh in mon_hoc_db if mh["ma_mon_hoc"] == kq["ma_mon_hoc"]), None)
            if mon_hoc:
                kq_with_mon_hoc = {
                    "mssv": kq["mssv"],
                    "ma_mon_hoc": kq["ma_mon_hoc"],
                    "ten_mon_hoc": mon_hoc["ten_mon_hoc"],
                    "diem_qua_trinh": kq["diem_qua_trinh"],
                    "diem_kiem_tra": kq["diem_kiem_tra"],
                    "diem_thi": kq["diem_thi"]
                }
                results.append(kq_with_mon_hoc)

    if not results:
        raise HTTPException(
            status_code=404, detail="Không tìm thấy kết quả học tập")
    return results


@router.post("/", response_model=KetQuaHocTap)
async def create_ket_qua(ket_qua: KetQuaHocTap):
    ket_qua_dict = ket_qua.dict()
    ket_qua_db.append(ket_qua_dict)
    save_ket_qua(ket_qua_db)
    return ket_qua_dict


@router.get("/sinh-vien/{mssv}/gpa", response_model=dict)
async def get_gpa_by_mssv(mssv: str):
    # Lấy dữ liệu mới nhất
    ket_qua_db = load_ket_qua()
    mon_hoc_db = load_mon_hoc()

    results = []
    for kq in ket_qua_db:
        if kq["mssv"] == mssv:
            # Tìm thông tin môn học
            mon_hoc = next(
                (mh for mh in mon_hoc_db if mh["ma_mon_hoc"] == kq["ma_mon_hoc"]), None)
            if mon_hoc:
                # Tính điểm trung bình môn
                diem_tb = (kq["diem_qua_trinh"] * 0.2 +
                           kq["diem_kiem_tra"] * 0.3 +
                           kq["diem_thi"] * 0.5)

                # Tính điểm chữ và GPA
                if diem_tb >= 9.0:
                    diem_chu = "A+"
                    gpa = 4.0
                elif diem_tb >= 8.5:
                    diem_chu = "A"
                    gpa = 3.7
                elif diem_tb >= 8.0:
                    diem_chu = "B+"
                    gpa = 3.5
                elif diem_tb >= 7.0:
                    diem_chu = "B"
                    gpa = 3.0
                elif diem_tb >= 6.5:
                    diem_chu = "C+"
                    gpa = 2.5
                elif diem_tb >= 5.5:
                    diem_chu = "C"
                    gpa = 2.0
                elif diem_tb >= 5.0:
                    diem_chu = "D+"
                    gpa = 1.5
                elif diem_tb >= 4.0:
                    diem_chu = "D"
                    gpa = 1.0
                else:
                    diem_chu = "F"
                    gpa = 0.0

                results.append({
                    "ma_mon_hoc": kq["ma_mon_hoc"],
                    "ten_mon_hoc": mon_hoc["ten_mon_hoc"],
                    "tin_chi": mon_hoc["tin_chi"],
                    "diem_trung_binh": round(diem_tb, 2),
                    "diem_chu": diem_chu,
                    "gpa": gpa
                })

    if not results:
        raise HTTPException(
            status_code=404, detail="Không tìm thấy kết quả học tập")

    # Tính GPA tổng
    tong_tin_chi = sum(r["tin_chi"] for r in results)
    tong_diem = sum(r["gpa"] * r["tin_chi"] for r in results)
    gpa_tong = round(tong_diem / tong_tin_chi, 2) if tong_tin_chi > 0 else 0

    return {
        "mssv": mssv,
        "chi_tiet_mon_hoc": results,
        "gpa_tong": gpa_tong,
        "tong_tin_chi": tong_tin_chi
    }


@router.put("/", response_model=KetQuaHocTap)
async def update_ket_qua(ket_qua: KetQuaHocTap):
    for i, kq in enumerate(ket_qua_db):
        if kq["mssv"] == ket_qua.mssv and kq["ma_mon_hoc"] == ket_qua.ma_mon_hoc:
            ket_qua_db[i] = ket_qua.dict()
            save_ket_qua(ket_qua_db)
            return ket_qua
    raise HTTPException(
        status_code=404, detail="Không tìm thấy kết quả học tập")


@router.delete("/{mssv}/{ma_mon_hoc}")
async def delete_ket_qua(mssv: str, ma_mon_hoc: str):
    for i, kq in enumerate(ket_qua_db):
        if kq["mssv"] == mssv and kq["ma_mon_hoc"] == ma_mon_hoc:
            ket_qua_db.pop(i)
            save_ket_qua(ket_qua_db)
            return {"message": "Đã xóa điểm thành công"}
    raise HTTPException(
        status_code=404, detail="Không tìm thấy kết quả học tập")


@router.get("/", response_model=List[KetQuaHocTap])
async def get_all_ket_qua():
    try:
        # Đọc dữ liệu từ file
        ket_qua_db = load_ket_qua()
        return ket_qua_db
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Không thể đọc dữ liệu kết quả: {str(e)}"
        )
