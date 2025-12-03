import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import csv
from typing import Tuple, Optional, Dict, Any

DATA_FILE = 'data.csv'
COLUMNS = ['Ma_SV', 'Ten', 'Toan', 'Ly', 'Hoa', 'Diem_TB', 'Xep_Loai']


def calculate_average_score(toan: float, ly: float, hoa: float) -> float:
    return round((toan + ly + hoa) / 3, 2)

def determine_rank(diem_tb: float) -> str:
    if diem_tb >= 8.0:
        return "Giỏi"
    elif diem_tb >= 6.5:
        return "Khá"
    elif diem_tb >= 5.0:
        return "Trung Bình"
    else:
        return "Yếu"

def validate_score(score_name: str, score: str) -> Optional[float]:
    try:
        score_float = float(score)
        if 0 <= score_float <= 10:
            return score_float
        else:
            print(f"Lỗi: Điểm {score_name} phải nằm trong khoảng [0, 10].")
            return None
    except ValueError:
        print(f"Lỗi: Điểm {score_name} không hợp lệ. Vui lòng nhập số.")
        return None


def load_data(filepath: str) -> pd.DataFrame:
    if os.path.exists(filepath):
        try:
            df = pd.read_csv(filepath)
            for col in COLUMNS:
                if col not in df.columns:
                    df[col] = None
            df = df.astype({'Ma_SV': str, 'Ten': str, 'Toan': float, 'Ly': float, 'Hoa': float, 'Diem_TB': float, 'Xep_Loai': str})
            print(f"\nĐã nạp {len(df)} sinh viên từ file '{filepath}'.")
            return df
        except pd.errors.EmptyDataError:
            print("\nFile dữ liệu rỗng. Khởi tạo danh sách sinh viên rỗng.")
            return pd.DataFrame(columns=COLUMNS)
        except Exception as e:
            print(f"\nLỗi khi đọc file CSV: {e}. Khởi tạo danh sách sinh viên rỗng.")
            return pd.DataFrame(columns=COLUMNS)
    else:
        print(f"\nFile '{filepath}' không tồn tại. Khởi tạo danh sách sinh viên rỗng.")
        return pd.DataFrame(columns=COLUMNS)

def save_data(df: pd.DataFrame, filepath: str):
    try:
        df[COLUMNS].to_csv(filepath, index=False, encoding='utf-8')
        print(f"\nĐã lưu danh sách sinh viên thành công vào file '{filepath}'.")
    except Exception as e:
        print(f"\nLỗi khi lưu dữ liệu vào file CSV: {e}")

def display_students(df: pd.DataFrame):
    print("\n--- DANH SÁCH SINH VIÊN ---")
    if df.empty:
        print("Danh sách sinh viên hiện đang trống.")
        return

    display_names = {
        'Ma_SV': 'Mã SV',
        'Ten': 'Họ Tên',
        'Toan': 'Toán',
        'Ly': 'Lý',
        'Hoa': 'Hoá',
        'Diem_TB': 'Điểm TB',
        'Xep_Loai': 'Xếp Loại'
    }

    df_display = df.rename(columns=display_names)
    print(df_display.to_string(index=False))
    print("-" * 70)


def add_student(df: pd.DataFrame) -> pd.DataFrame:
    print("\n--- THÊM MỚI SINH VIÊN ---")
    while True:
        ma_sv = input("Nhập Mã SV: ").strip().upper()
        if not ma_sv:
            print("Mã SV không được để trống.")
            continue
        if ma_sv in df['Ma_SV'].values:
            print("Lỗi: Mã SV đã tồn tại. Vui lòng nhập mã khác.")
            continue
        break

    ten = input("Nhập Họ Tên: ").strip()
    if not ten:
        ten = "No Name"

    while True:
        score_toan = validate_score("Toán", input("Nhập Điểm Toán (0-10): ").strip())
        if score_toan is None: continue

        score_ly = validate_score("Lý", input("Nhập Điểm Lý (0-10): ").strip())
        if score_ly is None: continue

        score_hoa = validate_score("Hoá", input("Nhập Điểm Hoá (0-10): ").strip())
        if score_hoa is None: continue
        break

    diem_tb = calculate_average_score(score_toan, score_ly, score_hoa)
    xep_loai = determine_rank(diem_tb)

    new_student = {
        'Ma_SV': ma_sv,
        'Ten': ten,
        'Toan': score_toan,
        'Ly': score_ly,
        'Hoa': score_hoa,
        'Diem_TB': diem_tb,
        'Xep_Loai': xep_loai
    }

    df_updated = pd.concat([df, pd.DataFrame([new_student])], ignore_index=True)

    print("\nThêm sinh viên thành công:")
    print(f"Mã SV: {ma_sv}, Tên: {ten}, Điểm TB: {diem_tb}, Xếp Loại: {xep_loai}")

    return df_updated

def update_student(df: pd.DataFrame) -> pd.DataFrame:
    print("\n--- CẬP NHẬT THÔNG TIN SINH VIÊN ---")
    if df.empty:
        print("Danh sách sinh viên trống. Không thể cập nhật.")
        return df

    ma_sv = input("Nhập Mã SV cần cập nhật: ").strip().upper()

    idx = df[df['Ma_SV'] == ma_sv].index
    if idx.empty:
        print(f"Lỗi: Không tìm thấy sinh viên có Mã SV: {ma_sv}")
        return df

    student_index = idx[0]
    student = df.loc[student_index]
    print(f"Đang cập nhật sinh viên: Mã SV={student['Ma_SV']}, Tên={student['Ten']}")

    while True:
        new_toan_str = input(f"Nhập Điểm Toán mới (Hiện tại: {student['Toan']}): ").strip()
        new_ly_str = input(f"Nhập Điểm Lý mới (Hiện tại: {student['Ly']}): ").strip()
        new_hoa_str = input(f"Nhập Điểm Hoá mới (Hiện tại: {student['Hoa']}): ").strip()

        score_toan = validate_score("Toán", new_toan_str) if new_toan_str else student['Toan']
        score_ly = validate_score("Lý", new_ly_str) if new_ly_str else student['Ly']
        score_hoa = validate_score("Hoá", new_hoa_str) if new_hoa_str else student['Hoa']

        if score_toan is not None and score_ly is not None and score_hoa is not None:
            break
        else:
            print("Vui lòng nhập lại toàn bộ điểm mới.")


    df.loc[student_index, 'Toan'] = score_toan
    df.loc[student_index, 'Ly'] = score_ly
    df.loc[student_index, 'Hoa'] = score_hoa

    diem_tb = calculate_average_score(score_toan, score_ly, score_hoa)
    xep_loai = determine_rank(diem_tb)

    df.loc[student_index, 'Diem_TB'] = diem_tb
    df.loc[student_index, 'Xep_Loai'] = xep_loai

    print(f"\nCập nhật thành công cho Mã SV {ma_sv}. Điểm TB mới: {diem_tb}, Xếp loại mới: {xep_loai}")

    return df

def delete_student(df: pd.DataFrame) -> pd.DataFrame:
    print("\n--- XOÁ SINH VIÊN ---")
    if df.empty:
        print("Danh sách sinh viên trống. Không thể xoá.")
        return df

    ma_sv = input("Nhập Mã SV cần xoá: ").strip().upper()

    idx = df[df['Ma_SV'] == ma_sv].index
    if idx.empty:
        print(f"Lỗi: Không tìm thấy sinh viên có Mã SV: {ma_sv}")
        return df

    student = df.loc[idx[0]]
    confirm = input(f"Bạn có chắc muốn xoá sinh viên '{student['Ten']}' (Mã SV: {ma_sv})? (y/n): ").strip().lower()

    if confirm == 'y':
        df_updated = df.drop(idx).reset_index(drop=True)
        print(f"Đã xoá sinh viên có Mã SV: {ma_sv}")
        return df_updated
    else:
        print("Huỷ bỏ thao tác xoá.")
        return df

def search_student(df: pd.DataFrame):
    print("\n--- TÌM KIẾM SINH VIÊN ---")
    if df.empty:
        print("Danh sách sinh viên trống. Không thể tìm kiếm.")
        return

    search_term = input("Nhập Mã SV HOẶC Tên (một phần) để tìm kiếm: ").strip()

    if not search_term:
        print("Vui lòng nhập từ khoá tìm kiếm.")
        return

    results = df[
        (df['Ma_SV'].str.upper() == search_term.upper()) |
        (df['Ten'].str.contains(search_term, case=False, na=False))
    ]

    if results.empty:
        print(f"Không tìm thấy sinh viên nào với từ khoá '{search_term}'.")
    else:
        print(f"--- KẾT QUẢ TÌM KIẾM ({len(results)} sinh viên) ---")
        display_students(results)


def sort_students(df: pd.DataFrame) -> pd.DataFrame:
    print("\n--- SẮP XẾP DANH SÁCH SINH VIÊN ---")
    if df.empty:
        print("Danh sách sinh viên trống. Không thể sắp xếp.")
        return df

    print("Chọn tiêu chí sắp xếp:")
    print("1. Điểm TB Giảm dần (Cao -> Thấp)")
    print("2. Tên Tăng dần (A -> Z)")

    choice = input("Nhập lựa chọn (1 hoặc 2): ").strip()
    df_sorted = df.copy()

    if choice == '1':
        df_sorted = df_sorted.sort_values(by='Diem_TB', ascending=False).reset_index(drop=True)
        print("\nDanh sách sinh viên đã được sắp xếp theo Điểm TB giảm dần.")
    elif choice == '2':
        df_sorted = df_sorted.sort_values(by='Ten', ascending=True).reset_index(drop=True)
        print("\nDanh sách sinh viên đã được sắp xếp theo Tên tăng dần (A-Z).")
    else:
        print("Lựa chọn không hợp lệ. Huỷ sắp xếp.")
        return df

    display_students(df_sorted)
    return df_sorted 

def get_statistics(df: pd.DataFrame) -> Tuple[Dict[str, int], int]:
    print("\n--- THỐNG KÊ ĐIỂM TRUNG BÌNH ---")
    if df.empty:
        print("Danh sách sinh viên trống. Không thể thống kê.")
        return {}, 0

    if 'Diem_TB' in df.columns:
        df['Xep_Loai'] = df['Diem_TB'].apply(determine_rank)

    rank_counts = df['Xep_Loai'].value_counts().to_dict()

    ranks = ["Giỏi", "Khá", "Trung Bình", "Yếu"]
    stats = {rank: rank_counts.get(rank, 0) for rank in ranks}
    total_students = len(df)

    print(f"Tổng số sinh viên: {total_students}")
    print("Thống kê Xếp loại học lực:")
    for rank, count in stats.items():
        percentage = (count / total_students * 100) if total_students > 0 else 0
        print(f"- Loại {rank}: {count} sinh viên ({percentage:.2f}%)")

    return stats, total_students


def plot_statistics(stats: Dict[str, int], total_students: int):
    if not stats:
        print("Không có dữ liệu thống kê để vẽ biểu đồ.")
        return

    labels = [k for k, v in stats.items() if v > 0]
    sizes = [v for v in stats.values() if v > 0]
    
    rank_colors = {
        "Giỏi": "#4CAF50",      
        "Khá": "#2196F3",       
        "Trung Bình": "#FFC107", 
        "Yếu": "#F44336"         
    }
    
    colors = [rank_colors[label] for label in labels]

    sns.set_theme(style="whitegrid")
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Biểu Đồ Thống Kê Xếp Loại Học Lực Sinh Viên', fontsize=16, y=1.02)
    
    wedges, texts, autotexts = axes[0].pie(
        sizes, 
        labels=labels, 
        colors=colors, 
        autopct='%1.1f%%',
        startangle=90, 
        wedgeprops={'edgecolor': 'black', 'linewidth': 0.5},
        textprops={'fontsize': 10}
    )
    axes[0].set_title(f'Tỷ Lệ Xếp Loại (Tổng: {total_students} SV)', fontsize=12)
    axes[0].axis('equal') 
    sns.barplot(
        x=labels, 
        y=sizes, 
        ax=axes[1], 
        palette=colors,
        edgecolor='black'
    )
    axes[1].set_title('Số Lượng Sinh Viên Theo Xếp Loại', fontsize=12)
    axes[1].set_ylabel('Số lượng sinh viên', fontsize=10)
    axes[1].set_xlabel('Xếp loại', fontsize=10)

    for i, v in enumerate(sizes):
        axes[1].text(i, v + 0.5, str(v), ha='center', va='bottom', fontsize=10)

    plt.tight_layout() 
    plt.show()
    
    print("\nĐã vẽ biểu đồ thống kê (Biểu đồ tròn và Biểu đồ cột).")


def display_menu():
    print("\n" + "="*40)
    print("     CHƯƠNG TRÌNH QUẢN LÝ SINH VIÊN")
    print("="*40)
    print("1. Hiển thị danh sách sinh viên")
    print("2. Thêm mới sinh viên")
    print("3. Cập nhật thông tin sinh viên")
    print("4. Xoá sinh viên")
    print("5. Tìm kiếm sinh viên")
    print("6. Sắp xếp danh sách sinh viên")
    print("7. Thống kê điểm TB")
    print("8. Vẽ biểu đồ thống kê điểm TB")
    print("9. Lưu vào file CSV")
    print("10. Thoát")
    print("="*40)

def main():
    student_df = load_data(DATA_FILE)

    while True:
        display_menu()
        choice = input("Nhập lựa chọn của bạn (1-10): ").strip()

        if choice == '1':
            display_students(student_df)
        elif choice == '2':
            student_df = add_student(student_df)
        elif choice == '3':
            student_df = update_student(student_df)
        elif choice == '4':
            student_df = delete_student(student_df)
        elif choice == '5':
            search_student(student_df)
        elif choice == '6':
            sort_students(student_df)
        elif choice == '7':
            get_statistics(student_df)
        elif choice == '8':
            stats, total = get_statistics(student_df)
            plot_statistics(stats, total)
        elif choice == '9':
            save_data(student_df, DATA_FILE)
        elif choice == '10':
            print("\nĐang lưu dữ liệu trước khi thoát...")
            save_data(student_df, DATA_FILE)
            print("Cảm ơn bạn đã sử dụng chương trình. Tạm biệt!")
            break
        else:
            print("\nLựa chọn không hợp lệ. Vui lòng chọn lại (1-10).")

if __name__ == "__main__":
    main()