from pydantic import BaseModel
from typing import Optional, List


class SinhVienBase(BaseModel):
    ten: str
    email: str
    sdt: str
    gioitinh: str
    mssv: str


class MonHocBase(BaseModel):
    ma_mon_hoc: str
    ten_mon_hoc: str
    tin_chi: int


class KetQuaHocTap(BaseModel):
    mssv: str
    ma_mon_hoc: str
    diem_qua_trinh: float
    diem_kiem_tra: float
    diem_thi: float

    def tinh_diem_trung_binh(self) -> float:
        # Tính theo trọng số: quá trình 20%, kiểm tra 30%, thi 50%
        return (self.diem_qua_trinh * 0.2 +
                self.diem_kiem_tra * 0.3 +
                self.diem_thi * 0.5)

    def xep_loai(self) -> str:
        diem = self.tinh_diem_trung_binh()
        if diem >= 9.0:
            return "A+"
        elif diem >= 8.5:
            return "A"
        elif diem >= 8.0:
            return "B+"
        elif diem >= 7.0:
            return "B"
        elif diem >= 6.5:
            return "C+"
        elif diem >= 5.5:
            return "C"
        elif diem >= 5.0:
            return "D+"
        elif diem >= 4.0:
            return "D"
        else:
            return "F"

    def to_gpa(self) -> float:
        # Chuyển điểm số sang hệ 4
        diem = self.tinh_diem_trung_binh()
        if diem >= 9.0:
            return 4.0
        elif diem >= 8.5:
            return 3.7
        elif diem >= 8.0:
            return 3.5
        elif diem >= 7.0:
            return 3.0
        elif diem >= 6.5:
            return 2.5
        elif diem >= 5.5:
            return 2.0
        elif diem >= 5.0:
            return 1.5
        elif diem >= 4.0:
            return 1.0
        else:
            return 0.0


class KetQuaChiTiet(BaseModel):
    ma_mon_hoc: str
    ten_mon_hoc: str
    tin_chi: int
    diem_qua_trinh: float
    diem_kiem_tra: float
    diem_thi: float
    diem_trung_binh: float
    diem_chu: str
    gpa: float


class KetQuaTongHop(BaseModel):
    mssv: str
    chi_tiet_mon_hoc: List[KetQuaChiTiet]
    gpa_tong: float
    tong_tin_chi: int
