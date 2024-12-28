import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from config import API_URL


class Viewer:
    def __init__(self):
        self.api_url = API_URL

    def get_sinh_vien_data(self):
        try:
            response = requests.get(f"{self.api_url}/sinh-vien")
            return response.json()
        except:
            st.error("Không thể kết nối với API")
            return []

    def get_mon_hoc_data(self):
        try:
            response = requests.get(f"{self.api_url}/mon-hoc")
            return response.json()
        except:
            st.error("Không thể kết nối với API")
            return []

    def get_ket_qua_data(self, mssv):
        try:
            response = requests.get(f"{self.api_url}/ket-qua/sinh-vien/{mssv}")
            return response.json()
        except:
            st.error("Không thể kết nối với API")
            return []

    def create_sinh_vien(self, sinh_vien_data):
        response = requests.post(
            f"{self.api_url}/sinh-vien",
            json=sinh_vien_data
        )
        return response.json()

    def NhapDuLieuSinhVien(self):
        st.subheader("📝 Quản lý thông tin Sinh viên")

        tab1, tab2 = st.tabs(["Danh sách sinh viên", "Thêm sinh viên mới"])

        with tab1:
            # Hiển thị danh sách sinh viên với khả năng chỉnh sửa
            sinh_vien_data = self.get_sinh_vien_data()
            if sinh_vien_data:
                df = pd.DataFrame(sinh_vien_data)
                edited_df = st.data_editor(
                    df,
                    column_config={
                        "ten": st.column_config.TextColumn(
                            "Họ và tên",
                            width="large",
                        ),
                        "email": st.column_config.TextColumn(
                            "Email",
                            width="medium",
                        ),
                        "sdt": st.column_config.TextColumn(
                            "Số điện thoại",
                            width="medium",
                        ),
                        "gioitinh": st.column_config.SelectboxColumn(
                            "Giới tính",
                            options=["Nam", "Nữ"],
                            width="small",
                        ),
                        "mssv": st.column_config.TextColumn(
                            "MSSV",
                            width="small",
                            disabled=True,
                        ),
                    },
                    hide_index=True,
                    num_rows="dynamic",
                    key="danh_sach_sinh_vien"
                )

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Lưu thay đổi", type="primary"):
                        try:
                            for _, row in edited_df.iterrows():
                                response = requests.put(
                                    f"{self.api_url}/sinh-vien/{row['mssv']}",
                                    json={
                                        "ten": row['ten'],
                                        "email": row['email'],
                                        "sdt": row['sdt'],
                                        "gioitinh": row['gioitinh'],
                                        "mssv": row['mssv']
                                    }
                                )
                            st.success(
                                "Đã cập nhật thông tin sinh viên thành công!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Lỗi khi cập nhật thông tin: {str(e)}")
            else:
                st.info("Chưa có dữ liệu sinh viên")

        with tab2:
            # Form thêm sinh viên mới
            with st.form("them_sinh_vien"):
                ten = st.text_input("Họ và tên")
                col1, col2 = st.columns(2)
                with col1:
                    email = st.text_input("Email")
                    gioitinh = st.selectbox("Giới tính", ["Nam", "Nữ"])
                with col2:
                    sdt = st.text_input("Số điện thoại")
                    mssv = st.text_input("Mã số sinh viên")

                submitted = st.form_submit_button("Thêm sinh viên")
                if submitted:
                    if not ten or not mssv:
                        st.error("Vui lòng nhập đầy đủ họ tên và MSSV!")
                    else:
                        sinh_vien_data = {
                            "ten": ten,
                            "email": email,
                            "sdt": sdt,
                            "gioitinh": gioitinh,
                            "mssv": mssv
                        }
                        try:
                            # Kiểm tra MSSV đã tồn tại chưa
                            existing_sv = [
                                sv for sv in self.get_sinh_vien_data() if sv['mssv'] == mssv]
                            if existing_sv:
                                st.error(f"MSSV {mssv} đã tồn tại!")
                            else:
                                response = self.create_sinh_vien(
                                    sinh_vien_data)
                                if response:
                                    st.success("Đã thêm sinh viên thành công!")
                                    st.rerun()
                        except Exception as e:
                            st.error(f"Lỗi khi thêm sinh viên: {str(e)}")

    def SuaThongTinSinhVien(self):
        sinh_vien_data = self.get_sinh_vien_data()
        if not sinh_vien_data:
            st.error("Không thể tải dữ liệu sinh viên")
            return

        # Chọn sinh viên để sửa
        selected_sv = st.selectbox(
            "Chọn sinh viên cần sửa",
            sinh_vien_data,
            format_func=lambda x: f"{x['ten']} ({x['mssv']})"
        )

        if selected_sv:
            with st.form("sua_sinh_vien"):
                col1, col2 = st.columns(2)
                with col1:
                    ten = st.text_input("Họ và tên", value=selected_sv['ten'])
                    email = st.text_input("Email", value=selected_sv['email'])
                    gioitinh = st.selectbox("Giới tính", ["Nam", "Nữ"],
                                            index=0 if selected_sv['gioitinh'] == "Nam" else 1)
                with col2:
                    sdt = st.text_input(
                        "Số điện thoại", value=selected_sv['sdt'])
                    mssv = st.text_input(
                        "Mã số sinh viên", value=selected_sv['mssv'], disabled=True)

                submitted = st.form_submit_button("Cập nhật thông tin")
                if submitted:
                    if not ten:
                        st.error("Vui lòng nhập họ tên!")
                    else:
                        sinh_vien_data = {
                            "ten": ten,
                            "email": email,
                            "sdt": sdt,
                            "gioitinh": gioitinh,
                            "mssv": mssv
                        }
                        try:
                            response = requests.put(
                                f"{self.api_url}/sinh-vien/{mssv}",
                                json=sinh_vien_data
                            )
                            if response.status_code == 200:
                                st.success(
                                    "Đã cập nhật thông tin sinh viên thành công!")
                                st.rerun()
                            else:
                                st.error(
                                    "Không thể cập nhật thông tin sinh viên")
                        except Exception as e:
                            st.error(f"Lỗi khi cập nhật thông tin: {str(e)}")

    def XemKetQuaHocTap(self):
        st.subheader("📊 Kết Quả Học Tập")
        self.XemDiem()

    def XemDiem(self):
        sinh_vien_data = self.get_sinh_vien_data()
        if not sinh_vien_data:
            st.error("Không thể tải dữ liệu sinh viên")
            return

        # Lấy tất cả kết quả học tập
        try:
            response = requests.get(f"{self.api_url}/ket-qua")
            ket_qua_data = response.json()
        except:
            st.error("Không thể tải dữ liệu kết quả")
            return

        # Chọn sinh viên để xem điểm
        selected_sv = st.selectbox(
            "Chọn sinh viên để xem điểm",
            sinh_vien_data,
            format_func=lambda x: f"{x['ten']} ({x['mssv']})"
        )

        if selected_sv:
            try:
                # Lấy danh sách môn học
                mon_hoc_data = self.get_mon_hoc_data()

                # Tạo DataFrame với tất cả môn học, mặc định điểm = 0
                df_all = pd.DataFrame([{
                    'ma_mon_hoc': mh['ma_mon_hoc'],
                    'ten_mon_hoc': mh['ten_mon_hoc'],
                    'tin_chi': mh['tin_chi'],
                    'diem_qua_trinh': 0.0,
                    'diem_kiem_tra': 0.0,
                    'diem_thi': 0.0,
                    'diem_trung_binh': 0.0,
                    'diem_chu': 'F',
                    'gpa': 0.0
                } for mh in mon_hoc_data])

                # Cập nhật điểm cho các môn đã có điểm
                diem_sv = [kq for kq in ket_qua_data if kq['mssv'] == selected_sv['mssv']]
                if diem_sv:
                    for diem in diem_sv:
                        mask = df_all['ma_mon_hoc'] == diem['ma_mon_hoc']
                        df_all.loc[mask, [
                            'diem_qua_trinh',
                            'diem_kiem_tra',
                            'diem_thi'
                        ]] = [
                            diem['diem_qua_trinh'],
                            diem['diem_kiem_tra'],
                            diem['diem_thi']
                        ]
                        # Tính điểm trung bình
                        diem_tb = (diem['diem_qua_trinh'] * 0.2 +
                                  diem['diem_kiem_tra'] * 0.3 +
                                  diem['diem_thi'] * 0.5)
                        df_all.loc[mask, 'diem_trung_binh'] = round(diem_tb, 2)

                        # Tính điểm chữ và GPA
                        if diem_tb >= 9.0:
                            diem_chu, gpa = 'A+', 4.0
                        elif diem_tb >= 8.5:
                            diem_chu, gpa = 'A', 3.7
                        elif diem_tb >= 8.0:
                            diem_chu, gpa = 'B+', 3.5
                        elif diem_tb >= 7.0:
                            diem_chu, gpa = 'B', 3.0
                        elif diem_tb >= 6.5:
                            diem_chu, gpa = 'C+', 2.5
                        elif diem_tb >= 5.5:
                            diem_chu, gpa = 'C', 2.0
                        elif diem_tb >= 5.0:
                            diem_chu, gpa = 'D+', 1.5
                        elif diem_tb >= 4.0:
                            diem_chu, gpa = 'D', 1.0
                        else:
                            diem_chu, gpa = 'F', 0.0

                        df_all.loc[mask, ['diem_chu', 'gpa']] = [diem_chu, gpa]

                # Tính GPA tổng và tổng tín chỉ
                df_co_diem = df_all[df_all['gpa'] > 0]
                tong_tin_chi = df_co_diem['tin_chi'].sum()
                gpa_tong = round((df_co_diem['gpa'] * df_co_diem['tin_chi']).sum() / 
                                tong_tin_chi, 2) if tong_tin_chi > 0 else 0.0

                # Hiển thị thông tin tổng quát
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("GPA Tổng", f"{gpa_tong:.2f}/4.0")
                with col2:
                    st.metric("Tổng số tín chỉ đã học", tong_tin_chi)
                with col3:
                    xep_loai = "Xuất sắc" if gpa_tong >= 3.7 else \
                              "Giỏi" if gpa_tong >= 3.5 else \
                              "Khá" if gpa_tong >= 3.0 else \
                              "Trung bình" if gpa_tong >= 2.0 else "Yếu"
                    st.metric("Xếp loại", xep_loai)

                # Hiển thị bảng điểm chi tiết
                st.subheader("Bảng điểm chi tiết")
                st.dataframe(
                    df_all,
                    column_config={
                        "ten_mon_hoc": "Tên môn học",
                        "tin_chi": "Số tín chỉ",
                        "diem_qua_trinh": "Điểm quá trình",
                        "diem_kiem_tra": "Điểm kiểm tra",
                        "diem_thi": "Điểm thi",
                        "diem_trung_binh": st.column_config.NumberColumn(
                            "Điểm TB",
                            format="%.2f"
                        ),
                        "diem_chu": "Điểm chữ",
                        "gpa": st.column_config.NumberColumn(
                            "GPA",
                            format="%.2f"
                        )
                    },
                    hide_index=True,
                    use_container_width=True
                )

                # Hiển thị biểu đồ điểm
                if not df_co_diem.empty:
                    st.subheader("Biểu đồ điểm")
                    fig = px.bar(
                        df_co_diem,
                        x='gpa',
                        y='ten_mon_hoc',
                        orientation='h',
                        title='GPA theo môn học'
                    )
                    fig.update_layout(
                        height=400,
                        showlegend=False,
                        yaxis={'categoryorder': 'total ascending'},
                        xaxis_title="GPA (thang 4)",
                        yaxis_title="",
                        title_x=0.5
                    )
                    fig.update_traces(
                        texttemplate='%{x:.2f}',
                        textposition='outside'
                    )
                    st.plotly_chart(fig, use_container_width=True)

            except Exception as e:
                st.error(f"Có lỗi xảy ra: {str(e)}")

    def NhapDiem(self):
        sinh_vien_data = self.get_sinh_vien_data()
        mon_hoc_data = self.get_mon_hoc_data()

        if not sinh_vien_data or not mon_hoc_data:
            st.error("Không thể tải dữ liệu")
            return

        # Chọn sinh viên
        selected_sv = st.selectbox(
            "Chọn sinh viên",
            sinh_vien_data,
            format_func=lambda x: f"{x['ten']} ({x['mssv']})",
            key="nhap_diem_sv"
        )

        if selected_sv:
            # Form nhập điểm
            with st.form("nhap_diem"):
                # Chọn môn học
                selected_mh = st.selectbox(
                    "Chọn môn học",
                    mon_hoc_data,
                    format_func=lambda x: f"{
                        x['ten_mon_hoc']} ({x['ma_mon_hoc']})"
                )

                col1, col2, col3 = st.columns(3)
                with col1:
                    diem_qt = st.number_input(
                        "Điểm quá trình",
                        min_value=0.0,
                        max_value=10.0,
                        step=0.1
                    )
                with col2:
                    diem_kt = st.number_input(
                        "Điểm kiểm tra",
                        min_value=0.0,
                        max_value=10.0,
                        step=0.1
                    )
                with col3:
                    diem_thi = st.number_input(
                        "Điểm thi",
                        min_value=0.0,
                        max_value=10.0,
                        step=0.1
                    )

                submitted = st.form_submit_button("Lưu điểm")

                if submitted:
                    try:
                        # Kiểm tra điểm hợp lệ
                        if not (0 <= diem_qt <= 10 and 0 <= diem_kt <= 10 and 0 <= diem_thi <= 10):
                            st.error("Điểm phải nằm trong khoảng 0-10")
                            return

                        # Tạo dữ liệu điểm
                        ket_qua_data = {
                            "mssv": selected_sv["mssv"],
                            "ma_mon_hoc": selected_mh["ma_mon_hoc"],
                            "diem_qua_trinh": diem_qt,
                            "diem_kiem_tra": diem_kt,
                            "diem_thi": diem_thi
                        }

                        # Gửi request tạo/cập nhật điểm
                        response = requests.put(
                            f"{self.api_url}/ket-qua",
                            json=ket_qua_data
                        )

                        if response.status_code == 200:
                            st.success(f"Đã lưu điểm môn {selected_mh['ten_mon_hoc']} cho sinh viên {
                                       selected_sv['ten']}")
                            st.rerun()
                        else:
                            st.error("Không thể lưu điểm. Vui lòng thử lại")

                    except Exception as e:
                        st.error(f"Có lỗi xảy ra: {str(e)}")
