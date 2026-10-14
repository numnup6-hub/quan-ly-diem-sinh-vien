import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Quản lý điểm sinh viên",
    page_icon="🎓",
    layout="wide",
)

st.markdown("""
<style>
    .main { background-color: #f6f8fc; }
    .block-container { padding-top: 1.8rem; padding-bottom: 2rem; }
    h1 { color: #163b70; }
    div[data-testid="stMetric"] {
        background: white; border: 1px solid #e4eaf4;
        padding: 16px; border-radius: 14px;
    }
    div[data-testid="stDataFrame"] {
        border: 1px solid #e4eaf4; border-radius: 12px;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎓 QUẢN LÝ ĐIỂM SINH VIÊN")
st.caption("Theo dõi điểm số • Tính điểm tổng kết • Xếp loại • Thống kê")

DEFAULT_DATA = [
    {"Ho_ten": "Ngọc", "Chuyen_can": 9, "Giua_ky": 7, "Cuoi_ky": 8},
    {"Ho_ten": "Nhi", "Chuyen_can": 8, "Giua_ky": 8, "Cuoi_ky": 5},
    {"Ho_ten": "Hương", "Chuyen_can": 7, "Giua_ky": 9, "Cuoi_ky": 7},
    {"Ho_ten": "Khang", "Chuyen_can": 7, "Giua_ky": 8, "Cuoi_ky": 9},
    {"Ho_ten": "Nam", "Chuyen_can": 8, "Giua_ky": 3, "Cuoi_ky": 5},
    {"Ho_ten": "Hoa", "Chuyen_can": 5, "Giua_ky": 9, "Cuoi_ky": 4},
    {"Ho_ten": "Khôi", "Chuyen_can": 9, "Giua_ky": 6, "Cuoi_ky": 5},
    {"Ho_ten": "Linh", "Chuyen_can": 4, "Giua_ky": 9, "Cuoi_ky": 7},
    {"Ho_ten": "Việt", "Chuyen_can": 7, "Giua_ky": 6, "Cuoi_ky": 9},
    {"Ho_ten": "Lan", "Chuyen_can": 8, "Giua_ky": 9, "Cuoi_ky": 8},
]

if "students" not in st.session_state:
    st.session_state.students = pd.DataFrame(DEFAULT_DATA)

def calculate(df):
    result = df.copy()
    result["Tong_ket"] = (
        0.2 * result["Chuyen_can"]
        + 0.3 * result["Giua_ky"]
        + 0.5 * result["Cuoi_ky"]
    ).round(2)

    def xep_loai(diem):
        if diem >= 8.5:
            return "Giỏi"
        elif diem >= 7:
            return "Khá"
        elif diem >= 5:
            return "Trung bình"
        return "Yếu"

    result["Xep_loai"] = result["Tong_ket"].apply(xep_loai)
    return result

df = calculate(st.session_state.students)

with st.sidebar:
    st.header("⚙️ Menu")
    page = st.radio(
        "Chọn chức năng",
        ["Tổng quan", "Danh sách điểm", "Thêm sinh viên", "Xóa sinh viên", "Tra cứu", "Biểu đồ"],
    )
    st.divider()
    st.info("Cách tính điểm: Chuyên cần 20% + Giữa kỳ 30% + Cuối kỳ 50%.")
    csv_data = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "📥 Tải bảng điểm CSV",
        data=csv_data,
        file_name="bang_diem_sinh_vien.csv",
        mime="text/csv",
        use_container_width=True,
    )

if page == "Tổng quan":
    st.subheader("Tổng quan lớp học")
    best = df.loc[df["Tong_ket"].idxmax()]
    worst = df.loc[df["Tong_ket"].idxmin()]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Tổng sinh viên", len(df))
    c2.metric("Điểm trung bình lớp", f"{df['Tong_ket'].mean():.2f}")
    c3.metric("Sinh viên đạt", f"{(df['Tong_ket'] >= 5).sum()}/{len(df)}")
    c4.metric("Điểm cao nhất", f"{best['Tong_ket']:.2f}")
    left, right = st.columns(2)
    with left:
        st.markdown("#### 🏆 Điểm cao nhất")
        st.write(f"**{best['Ho_ten']}** — {best['Tong_ket']:.2f} điểm")
    with right:
        st.markdown("#### 📌 Điểm thấp nhất")
        st.write(f"**{worst['Ho_ten']}** — {worst['Tong_ket']:.2f} điểm")
    st.markdown("#### Bảng điểm mới nhất")
    st.dataframe(df, use_container_width=True, hide_index=True)

elif page == "Danh sách điểm":
    st.subheader("📋 Bảng điểm sinh viên")
    st.caption("Điểm tổng kết được tính tự động theo trọng số 20% – 30% – 50%.")
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.download_button(
        "Xuất bảng điểm Excel-compatible (CSV)",
        data=df.to_csv(index=False).encode("utf-8-sig"),
        file_name="bang_diem_sinh_vien.csv",
        mime="text/csv",
    )

elif page == "Thêm sinh viên":
    st.subheader("➕ Thêm sinh viên")
    with st.form("add_student_form", clear_on_submit=True):
        name = st.text_input("Họ và tên")
        a, b, c = st.columns(3)
        with a:
            attendance = st.number_input("Điểm chuyên cần", min_value=0.0, max_value=10.0, step=0.5)
        with b:
            midterm = st.number_input("Điểm giữa kỳ", min_value=0.0, max_value=10.0, step=0.5)
        with c:
            final = st.number_input("Điểm cuối kỳ", min_value=0.0, max_value=10.0, step=0.5)
        submitted = st.form_submit_button("Thêm vào danh sách", use_container_width=True)
        if submitted:
            if not name.strip():
                st.error("Mày nhập họ tên sinh viên trước nha.")
            elif st.session_state.students["Ho_ten"].str.casefold().eq(name.strip().casefold()).any():
                st.error("Tên sinh viên này đã có trong danh sách.")
            else:
                new_row = pd.DataFrame([{
                    "Ho_ten": name.strip(),
                    "Chuyen_can": attendance,
                    "Giua_ky": midterm,
                    "Cuoi_ky": final,
                }])
                st.session_state.students = pd.concat(
                    [st.session_state.students, new_row], ignore_index=True
                )
                st.success(f"Đã thêm sinh viên {name.strip()}!")
                st.rerun()

elif page == "Xóa sinh viên":
    st.subheader("🗑️ Xóa sinh viên")
    if df.empty:
        st.info("Danh sách hiện chưa có sinh viên.")
    else:
        name_to_delete = st.selectbox("Chọn sinh viên cần xóa", df["Ho_ten"].tolist())
        st.warning(f"Mày đang chọn xóa sinh viên: **{name_to_delete}**.")
        if st.button("Xác nhận xóa", type="primary"):
            st.session_state.students = st.session_state.students[
                st.session_state.students["Ho_ten"] != name_to_delete
            ].reset_index(drop=True)
            st.success("Đã xóa sinh viên khỏi danh sách.")
            st.rerun()

elif page == "Tra cứu":
    st.subheader("🔎 Tra cứu điểm sinh viên")
    if df.empty:
        st.info("Chưa có dữ liệu để tra cứu.")
    else:
        name = st.selectbox("Chọn sinh viên", df["Ho_ten"].tolist())
        student = df[df["Ho_ten"] == name].iloc[0]
        a, b, c, d = st.columns(4)
        a.metric("Chuyên cần", f"{student['Chuyen_can']:.1f}")
        b.metric("Giữa kỳ", f"{student['Giua_ky']:.1f}")
        c.metric("Cuối kỳ", f"{student['Cuoi_ky']:.1f}")
        d.metric("Tổng kết", f"{student['Tong_ket']:.2f}")
        st.success(f"Xếp loại: **{student['Xep_loai']}**")

elif page == "Biểu đồ":
    st.subheader("📊 Biểu đồ điểm tổng kết")
    if df.empty:
        st.info("Chưa có dữ liệu để vẽ biểu đồ.")
    else:
        fig, ax = plt.subplots(figsize=(11, 5.5))
        bars = ax.bar(df["Ho_ten"], df["Tong_ket"])
        ax.set_title("Điểm tổng kết của sinh viên")
        ax.set_xlabel("Tên sinh viên")
        ax.set_ylabel("Điểm tổng kết")
        ax.set_ylim(0, 10)
        ax.grid(axis="y", linestyle="--", alpha=0.3)
        ax.bar_label(bars, fmt="%.2f", padding=3, fontsize=8)
        plt.xticks(rotation=35, ha="right")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

st.markdown("---")
st.markdown(
    "<p style='text-align:center;color:gray;font-size:12px;'>"
    "Ứng dụng được tạo bởi: Lê Nguyên Bảo Ngọc - MSSV: 034308016103"
    "</p>",
    unsafe_allow_html=True,
)
