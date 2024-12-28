import streamlit as st
from viewer import Viewer
import pandas as pd
import plotly.express as px
from PIL import Image
from pathlib import Path
import os


def main():
    st.set_page_config(
        page_title="Quản lý Sinh viên",
        page_icon="📚",
        layout="wide"
    )

    viewer = Viewer()

    # Khởi tạo session state nếu chưa có
    if 'sinh_vien_data' not in st.session_state:
        st.session_state.sinh_vien_data = viewer.get_sinh_vien_data()

    # Menu chính
    menu = ["Trang chủ", "Nhập sinh viên",
            "Sửa thông tin sinh viên",
            "Nhập điểm",
            "Xem kết quả học tập", "Thống kê & Đồ thị"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Trang chủ":
        st.title("🏫 Hệ thống Quản lý Sinh viên")
        st.write("Chọn chức năng từ menu bên trái để bắt đầu.")

        # Hiển thị dữ liệu sinh viên
        st.subheader("📋 Danh sách Sinh viên")
        if st.session_state.sinh_vien_data:
            df_sv = pd.DataFrame(st.session_state.sinh_vien_data)
            st.dataframe(df_sv, use_container_width=True)
        else:
            st.info("Chưa có dữ liệu sinh viên")

    elif choice == "Nhập sinh viên":
        st.subheader("📝 Nhập thông tin Sinh viên")
        viewer.NhapDuLieuSinhVien()
        # Cập nhật session state sau khi nhập
        st.session_state.sinh_vien_data = viewer.get_sinh_vien_data()

    elif choice == "Sửa thông tin sinh viên":
        st.subheader("✏️ Sửa thông tin Sinh viên")
        viewer.SuaThongTinSinhVien()
        # Cập nhật session state sau khi sửa
        st.session_state.sinh_vien_data = viewer.get_sinh_vien_data()

    elif choice == "Nhập điểm":
        st.subheader("📝 Nhập điểm")
        viewer.NhapDiem()

    elif choice == "Xem kết quả học tập":
        viewer.XemKetQuaHocTap()

    elif choice == "Thống kê & Đồ thị":
        st.subheader("📊 Thống kê & Đồ thị")

        # Lấy dữ liệu
        sinh_vien_data = viewer.get_sinh_vien_data()
        mon_hoc_data = viewer.get_mon_hoc_data()

        if sinh_vien_data and mon_hoc_data:
            df_sv = pd.DataFrame(sinh_vien_data)
            df_mh = pd.DataFrame(mon_hoc_data)

            # Thống kê theo giới tính
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Phân bố giới tính")
                fig_gender = px.pie(df_sv, names='gioitinh',
                                    title='Tỷ lệ sinh viên theo giới tính')
                st.plotly_chart(fig_gender, use_container_width=True)

            # Thống kê số tín chỉ theo môn học
            with col2:
                st.subheader("Phân bố tín chỉ")
                fig_credits = px.bar(df_mh,
                                     x='ten_mon_hoc',
                                     y='tin_chi',
                                     title='Số tín chỉ theo môn học')
                st.plotly_chart(fig_credits, use_container_width=True)

            # Thống kê số lượng sinh viên theo giới tính
            st.subheader("Thống kê chi tiết")
            col3, col4 = st.columns(2)

            with col3:
                gender_counts = df_sv['gioitinh'].value_counts()
                st.metric("Tổng số sinh viên", len(df_sv))
                st.write("Theo giới tính:")
                for gender, count in gender_counts.items():
                    st.write(f"- {gender}: {count} sinh viên")

            with col4:
                st.metric("Tổng số môn học", len(df_mh))
                total_credits = df_mh['tin_chi'].sum()
                st.metric("Tổng số tín chỉ", total_credits)
                avg_credits = df_mh['tin_chi'].mean()
                st.metric("Trung bình tín chỉ/môn", f"{avg_credits:.1f}")

        else:
            st.info("Cần có dữ liệu sinh viên và môn học để hiển thị thống kê")


if __name__ == "__main__":
    main()
