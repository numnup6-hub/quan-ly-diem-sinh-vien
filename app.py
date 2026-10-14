import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")

#1. Tạo DataFrame
data = {"Ho_ten":
 ["Ngọc", "Nhi", "Hương", "Khang", "Nam",
  "Hoa", "Khôi", "Linh", "Việt", "Lan"],
        "Chuyen_can": [9, 8, 7, 7, 8, 5, 9, 4, 7, 8],
        "Giua_ky":    [7, 8, 9, 8, 3, 9, 6, 9, 6, 9],
        "Cuoi_ky":    [8, 5, 7, 9, 5, 4, 5, 7, 9, 8],}
df = pd.DataFrame(data)
st.write("Bảng điểm của 10 sinh viên:")
st.write(df)
#2. Tính điểm tổng kết
df["Tong_ket"] = (
   0.2 * df["Chuyen_can"]
  + 0.3 * df["Giua_ky"]
  + 0.5 * df["Cuoi_ky"]
  )

df["Tong_ket"] = df["Tong_ket"].round(2)
st.write("Điểm tổng kết:")
st.write(df)
#3. Xếp loại sinh viên
def xep_loai(diem):

  if diem >= 8.5:
    return("Giỏi")
  elif diem >= 7.0:
    return("Khá")
  elif diem >= 5.0:
    return("Trung bình")
  else:
    return("Yếu")

df["Xep_loai"] = df["Tong_ket"].apply(xep_loai)
st.write("Xếp loại sinh viên:")
st.write(df)
#4. Thông kê
diem_tb = df["Tong_ket"].mean()
st.write("Điểm trung bình của lớp:", round(diem_tb, 2))

sv_cao_nhat = df.loc[df["Tong_ket"].idxmax()]
st.write("Sinh viên điểm cao nhất:")
st.write(sv_cao_nhat[["Ho_ten", "Tong_ket"]])

sv_thap_nhat = df.loc[df["Tong_ket"].idxmin()]
st.write("Sinh viên điểm thấp nhất:")
st.write(sv_thap_nhat[["Ho_ten", "Tong_ket"]])

so_sv_dat = (df["Tong_ket"] >= 5).sum()
st.write("Số sinh viên đạt:", so_sv_dat)

st.write("Tra cứu điểm sinh viên")
danh_sach_sv = df["Ho_ten"].tolist()
sinh_vien_duoc_chon = st.selectbox("Chọn sinh viên:",danh_sach_sv)

thong_tin_sv = df[df["Ho_ten"] == sinh_vien_duoc_chon].iloc[0]
st.write(f"Điểm chuyên cần:{thong_tin_sv['Chuyen_can']}")
st.write(f"Điểm giữa kỳ:{thong_tin_sv['Giua_ky']}")
st.write(f"Điểm cuối kỳ:{thong_tin_sv['Cuoi_ky']}")
st.write(f"Điểm tổng kết:{thong_tin_sv['Tong_ket']}")
st.write(f"Xếp loại:{thong_tin_sv['Xep_loai']}")

#5. Trực quan hóa
st.write("Biểu đồ điểm tổng kết của sinh viên")
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(df["Ho_ten"], 
        df["Tong_ket"])

ax.set_title("Điểm tổng kết của 10 sinh viên")
ax.set_xlabel("Tên sinh viên")
ax.set_ylabel("Điểm tổng kết")
ax.set_ylim(0, 10)
plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig)
plt.close(fig)

st.markdown("")
st.markdown("<p style='text-align: center; font-size: 12px; color: gray; '>Ứng dụng được tạo bởi: Lê Nguyên Bảo Ngọc - MSSV: 034308016103</p>", unsafe_allow_html=True)
