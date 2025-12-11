import json
import csv
from typing import List, Dict, Optional
import matplotlib.pyplot as plt


# ==================== File và dữ liệu ====================
studentList = []  # Danh sách lưu trữ tất cả sinh viên
DATA_FILE = "data.json"
CSV_FILE = "data.csv"


# ==================== Các hàm chính  ====================

def calculateAverage(mathScore: float,
                     physicsScore: float,
                     chemistryScore: float) -> float:
    """
    Tính điểm trung bình của sinh viên.

    Args:
        mathScore: Điểm Toán (0-10)
        physicsScore: Điểm Lý (0-10)
        chemistryScore: Điểm Hóa (0-10)

    Returns:
        Điểm trung bình làm tròn 2 chữ số thập phân
    """
    return round((mathScore + physicsScore + chemistryScore) / 3, 2)


def getGradeClassification(averageScore: float) -> str:
    """
    Xác định xếp loại học lực dựa trên điểm trung bình.

    Args:
        averageScore: Điểm trung bình của sinh viên

    Returns:
        Xếp loại học lực (Giỏi, Khá, Trung Bình, Yếu)
    """
    if averageScore >= 8.0:
        return "Giỏi"
    if averageScore >= 6.5:
        return "Khá"
    if averageScore >= 5.0:
        return "Trung Bình"
    return "Yếu"


def createStudent(studentId: str, name: str, mathScore: float,
                  physicsScore: float, chemistryScore: float) -> Dict:
    """
    Tạo dictionary chứa đầy đủ thông tin sinh viên.

    Args:
        studentId: Mã sinh viên (unique)
        name: Họ tên sinh viên
        mathScore: Điểm Toán (0-10)
        physicsScore: Điểm Lý (0-10)
        chemistryScore: Điểm Hóa (0-10)

    Returns:
        Dictionary chứa thông tin đầy đủ của sinh viên
    """
    avgScore = calculateAverage(mathScore, physicsScore, chemistryScore)
    return {
        "id": studentId,
        "name": name,
        "mathScore": mathScore,
        "physicsScore": physicsScore,
        "chemistryScore": chemistryScore,
        "averageScore": avgScore,
        "gradeClassification": getGradeClassification(avgScore)
    }


def validateScore(score: float) -> bool:
    """
    Kiểm tra điểm có hợp lệ không (trong khoảng 0-10).

    Args:
        score: Điểm cần kiểm tra

    Returns:
        True nếu hợp lệ, False nếu không hợp lệ
    """
    return 0 <= score <= 10


def validateStudentId(studentId: str) -> bool:
    """
    Kiểm tra mã sinh viên có bị trùng không.

    Args:
        studentId: Mã sinh viên cần kiểm tra

    Returns:
        True nếu mã chưa tồn tại, False nếu đã tồn tại
    """
    for student in studentList:
        if student["id"] == studentId:
            return False
    return True


def findStudentById(studentId: str) -> Optional[Dict]:
    """
    Tìm sinh viên theo mã sinh viên.

    Args:
        studentId: Mã sinh viên cần tìm

    Returns:
        Dictionary của sinh viên nếu tìm thấy, None nếu không tìm thấy
    """
    for student in studentList:
        if student["id"] == studentId:
            return student
    return None


def findStudentsByName(name: str) -> List[Dict]:
    """
    Tìm sinh viên theo tên (tìm kiếm gần đúng, không phân biệt hoa thường).

    Args:
        name: Tên hoặc một phần tên cần tìm

    Returns:
        Danh sách các sinh viên tìm được
    """
    result = []
    nameLower = name.lower()
    for student in studentList:
        if nameLower in student["name"].lower():
            result.append(student)
    return result


# ==================== FILE VÀ DỮ LIỆU ====================

def loadFromJson() -> bool:
    """
    Đọc dữ liệu sinh viên từ file JSON.

    Returns:
        True nếu đọc thành công, False nếu file không tồn tại hoặc lỗi
    """
    global studentList
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as file:
            studentList = json.load(file)
            print(f"Đã tải {len(studentList)} sinh viên từ {DATA_FILE}")
            return True
    except FileNotFoundError:
        return False
    except json.JSONDecodeError:
        print("Lỗi đọc file JSON.")
        return False


def loadFromCsv() -> bool:
    """
    Đọc dữ liệu sinh viên từ file CSV.

    Returns:
        True nếu đọc thành công, False nếu file không tồn tại hoặc lỗi
    """
    global studentList
    try:
        with open(CSV_FILE, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            studentList = []
            for row in reader:
                student = {
                    "id": row['id'],
                    "name": row['name'],
                    "mathScore": float(row['mathScore']),
                    "physicsScore": float(row['physicsScore']),
                    "chemistryScore": float(row['chemistryScore'])
                }
                avg = calculateAverage(
                    student["mathScore"],
                    student["physicsScore"],
                    student["chemistryScore"])
                student["averageScore"] = avg
                student["gradeClassification"] = getGradeClassification(avg)
                studentList.append(student)
            print(f"Đã tải {len(studentList)} sinh viên từ {CSV_FILE}")
            return True
    except FileNotFoundError:
        return False
    except Exception as e:
        print(f"Lỗi đọc file CSV: {e}")
        return False


def loadData():
    """
    Tải dữ liệu sinh viên từ file (ưu tiên JSON, sau đó CSV).
    Nếu cả hai file đều không tồn tại, khởi tạo danh sách rỗng.
    """
    if not loadFromJson():
        if not loadFromCsv():
            print("Không tìm thấy file dữ liệu. Khởi tạo danh sách rỗng.")


def saveToJson():
    """
    Lưu dữ liệu sinh viên vào file JSON.
    """
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as file:
            json.dump(studentList, file, ensure_ascii=False, indent=2)
        print(f"Đã lưu dữ liệu vào {DATA_FILE}")
    except Exception as e:
        print(f"Lỗi khi lưu dữ liệu: {e}")


def saveToCsv():
    """
    Lưu dữ liệu sinh viên vào file CSV.
    """
    try:
        if len(studentList) == 0:
            print("Không có dữ liệu để lưu.")
            return

        with open(CSV_FILE, 'w', encoding='utf-8', newline='') as file:
            fieldnames = ['id', 'name', 'mathScore', 'physicsScore',
                          'chemistryScore', 'averageScore',
                          'gradeClassification']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(studentList)
        print(f"Đã lưu dữ liệu vào {CSV_FILE}")
    except Exception as e:
        print(f"Lỗi khi lưu CSV: {e}")


# ==================== MENU FUNCTIONS ====================

def displayAllStudents():
    """
    Hiển thị danh sách tất cả sinh viên dạng bảng.
    """
    if len(studentList) == 0:
        print("\nDanh sách sinh viên trống!")
        return

    print("\n" + "="*110)
    print(f"{'STT':<5} {'Mã SV':<10} {'Tên':<25} {'Toán':<8} "
          f"{'Lý':<8} {'Hóa':<8} {'ĐTB':<8} {'Xếp loại':<12}")
    print("="*110)

    for idx, student in enumerate(studentList, 1):
        print(f"{idx:<5} {student['id']:<10} {student['name']:<25} "
              f"{student['mathScore']:<8.1f} {student['physicsScore']:<8.1f} "
              f"{student['chemistryScore']:<8.1f} "
              f"{student['averageScore']:<8.2f} "
              f"{student['gradeClassification']:<12}")

    print("="*110)
    print(f"Tổng số sinh viên: {len(studentList)}")


def addStudent():
    """
    Thêm sinh viên mới vào danh sách.
    Yêu cầu nhập đầy đủ thông tin và kiểm tra tính hợp lệ.
    """
    print("\n--- THÊM SINH VIÊN MỚI ---")

    # Nhập và kiểm tra mã sinh viên
    while True:
        studentId = input("Nhập mã sinh viên: ").strip()
        if not studentId:
            print("Mã sinh viên không được để trống!")
            continue
        if not validateStudentId(studentId):
            print("Mã sinh viên đã tồn tại!")
            continue
        break

    # Nhập tên sinh viên
    name = input("Nhập tên sinh viên: ").strip()
    while not name:
        print("Tên không được để trống!")
        name = input("Nhập tên sinh viên: ").strip()

    # Nhập điểm Toán
    while True:
        try:
            mathScore = float(input("Nhập điểm Toán (0-10): "))
            if not validateScore(mathScore):
                print("Điểm phải trong khoảng 0-10!")
                continue
            break
        except ValueError:
            print("Vui lòng nhập số hợp lệ!")

    # Nhập điểm Lý
    while True:
        try:
            physicsScore = float(input("Nhập điểm Lý (0-10): "))
            if not validateScore(physicsScore):
                print("Điểm phải trong khoảng 0-10!")
                continue
            break
        except ValueError:
            print("Vui lòng nhập số hợp lệ!")

    # Nhập điểm Hóa
    while True:
        try:
            chemistryScore = float(input("Nhập điểm Hóa (0-10): "))
            if not validateScore(chemistryScore):
                print("Điểm phải trong khoảng 0-10!")
                continue
            break
        except ValueError:
            print("Vui lòng nhập số hợp lệ!")

    # Tạo và thêm sinh viên mới
    newStudent = createStudent(
        studentId, name, mathScore, physicsScore, chemistryScore)
    studentList.append(newStudent)

    print(f"\nĐã thêm sinh viên: {name} (Mã: {studentId})")
    print(f"  Điểm TB: {newStudent['averageScore']} - "
          f"Xếp loại: {newStudent['gradeClassification']}")


def updateStudent():
    """
    Cập nhật thông tin sinh viên.
    Cho phép cập nhật từng trường hoặc giữ nguyên giá trị cũ.
    """
    print("\n--- CẬP NHẬT THÔNG TIN SINH VIÊN ---")

    studentId = input("Nhập mã sinh viên cần sửa: ").strip()
    student = findStudentById(studentId)

    if not student:
        print(f"Không tìm thấy sinh viên có mã: {studentId}")
        return

    # Hiển thị thông tin hiện tại
    print("Thông tin hiện tại:")
    print(f"Tên: {student['name']}")
    print(f"Điểm Toán: {student['mathScore']}")
    print(f"Điểm Lý: {student['physicsScore']}")
    print(f"Điểm Hóa: {student['chemistryScore']}")

    # Cập nhật tên
    newName = input("\nNhập tên mới (Enter để giữ nguyên): ").strip()
    if newName:
        student['name'] = newName

    # Cập nhật điểm Toán
    mathInput = input("Nhập điểm Toán mới (Enter để giữ nguyên): ").strip()
    if mathInput:
        try:
            mathScore = float(mathInput)
            if validateScore(mathScore):
                student['mathScore'] = mathScore
            else:
                print("Điểm không hợp lệ, giữ nguyên giá trị cũ")
        except ValueError:
            print("Điểm không hợp lệ, giữ nguyên giá trị cũ")

    # Cập nhật điểm Lý
    physicsInput = input("Nhập điểm Lý mới (Enter để giữ nguyên): ").strip()
    if physicsInput:
        try:
            physicsScore = float(physicsInput)
            if validateScore(physicsScore):
                student['physicsScore'] = physicsScore
            else:
                print("Điểm không hợp lệ, giữ nguyên giá trị cũ")
        except ValueError:
            print("Điểm không hợp lệ, giữ nguyên giá trị cũ")

    # Cập nhật điểm Hóa
    chemistryInput = input(
        "Nhập điểm Hóa mới (Enter để giữ nguyên): ").strip()
    if chemistryInput:
        try:
            chemistryScore = float(chemistryInput)
            if validateScore(chemistryScore):
                student['chemistryScore'] = chemistryScore
            else:
                print("Điểm không hợp lệ, giữ nguyên giá trị cũ")
        except ValueError:
            print("Điểm không hợp lệ, giữ nguyên giá trị cũ")

    # Cập nhật lại điểm TB và xếp loại
    avg = calculateAverage(
        student['mathScore'],
        student['physicsScore'],
        student['chemistryScore'])
    student['averageScore'] = avg
    student['gradeClassification'] = getGradeClassification(avg)

    print("Đã cập nhật thông tin sinh viên!")
    print(f"Điểm TB mới: {student['averageScore']} - "
          f"Xếp loại: {student['gradeClassification']}")


def deleteStudent():
    """
    Xóa sinh viên khỏi danh sách.
    Yêu cầu xác nhận trước khi xóa.
    """
    print("\n--- XÓA SINH VIÊN ---")

    studentId = input("Nhập mã sinh viên cần xóa: ").strip()
    student = findStudentById(studentId)

    if not student:
        print(f"Không tìm thấy sinh viên có mã: {studentId}")
        return

    # Hiển thị thông tin sinh viên sẽ bị xóa
    print("Thông tin sinh viên sẽ bị xóa:")
    print(f"Mã: {student['id']} - Tên: {student['name']}")

    confirm = input("Bạn có chắc muốn xóa? (yes/no): ").strip().lower()
    if confirm in ['yes', 'y', 'có']:
        studentList.remove(student)
        print(f"Đã xóa sinh viên: {student['name']}")
    else:
        print("Đã hủy thao tác xóa")


def searchStudent():
    """
    Tìm kiếm sinh viên theo tên hoặc mã.
    Hỗ trợ tìm kiếm gần đúng với tên.
    """
    print("\n--- TÌM KIẾM SINH VIÊN ---")
    keyword = input("Nhập tên hoặc mã sinh viên cần tìm: ").strip()

    # Tìm theo mã trước
    student = findStudentById(keyword)
    if student:
        print("\nTìm thấy sinh viên:")
        print(f"Mã SV: {student['id']} | Tên: {student['name']} | "
              f"Toán: {student['mathScore']} | "
              f"Lý: {student['physicsScore']} | "
              f"Hóa: {student['chemistryScore']} | "
              f"ĐTB: {student['averageScore']} | "
              f"Xếp loại: {student['gradeClassification']}")
        return

    # Tìm theo tên
    results = findStudentsByName(keyword)
    if len(results) > 0:
        print(f"\nTìm thấy {len(results)} sinh viên:")
        for student in results:
            print(f"Mã SV: {student['id']} | Tên: {student['name']} | "
                  f"Toán: {student['mathScore']} | "
                  f"Lý: {student['physicsScore']} |"
                  f"Hóa: {student['chemistryScore']} | "
                  f"ĐTB: {student['averageScore']} | "
                  f"Xếp loại: {student['gradeClassification']}")
    else:
        print(f"Không tìm thấy sinh viên nào với từ khóa: {keyword}")


def sortStudents():
    """
    Sắp xếp danh sách sinh viên theo điểm TB hoặc tên.
    """
    if len(studentList) == 0:
        print("\nDanh sách sinh viên trống!")
        return

    print("\n--- SẮP XẾP DANH SÁCH ---")
    print("1. Sắp xếp theo Điểm TB giảm dần")
    print("2. Sắp xếp theo Tên tăng dần (A-Z)")

    choice = input("Chọn cách sắp xếp (1-2): ").strip()

    match choice:
        case '1':
            studentList.sort(key=lambda x: x['averageScore'], reverse=True)
            print("Đã sắp xếp theo Điểm TB giảm dần")
        case '2':
            studentList.sort(key=lambda x: x['name'])
            print("Đã sắp xếp theo Tên tăng dần (A-Z)")
        case _:
            print("Lựa chọn không hợp lệ!")
            return

    displayAllStudents()


def displayStatistics():
    """
    Hiển thị thống kê điểm trung bình theo xếp loại.
    """
    if len(studentList) == 0:
        print("\nDanh sách sinh viên trống!")
        return

    print("\n--- THỐNG KÊ ĐIỂM TRUNG BÌNH ---")

    # Đếm số sinh viên theo xếp loại
    stats = {"Giỏi": 0, "Khá": 0, "Trung Bình": 0, "Yếu": 0}
    for student in studentList:
        stats[student['gradeClassification']] += 1

    print(f"\nTổng số sinh viên: {len(studentList)}")
    print(f"Giỏi: {stats['Giỏi']} sinh viên")
    print(f"Khá: {stats['Khá']} sinh viên")
    print(f"Trung Bình: {stats['Trung Bình']} sinh viên")
    print(f"Yếu: {stats['Yếu']} sinh viên")

    # Tính điểm TB chung
    totalAvg = sum(student['averageScore']
                   for student in studentList) / len(studentList)
    print(f"\nĐiểm trung bình chung: {totalAvg:.2f}")


def displayChart():
    """
    Vẽ biểu đồ thống kê xếp loại học lực bằng matplotlib.
    Hỗ trợ 2 loại biểu đồ: Pie Chart và Bar Chart.
    """
    if len(studentList) == 0:
        print("\nDanh sách sinh viên trống!")
        return

    print("\n--- Biểu đồ thống kê ---")
    print("1. Biểu đồ tròn (Pie Chart)")
    print("2. Biểu đồ cột (Bar Chart)")

    chartChoice = input("Chọn loại biểu đồ (1-2): ").strip()

    # Đếm số sinh viên theo xếp loại
    stats = {"Giỏi": 0, "Khá": 0, "Trung Bình": 0, "Yếu": 0}
    for student in studentList:
        stats[student['gradeClassification']] += 1

    # Lọc ra các xếp loại có sinh viên
    labels = []
    values = []
    for grade, count in stats.items():
        if count > 0:
            labels.append(grade)
            values.append(count)

    # Thiết lập font tiếng Việt
    plt.rcParams['font.family'] = 'DejaVu Sans'

    match chartChoice:
        case '1':
            # Vẽ biểu đồ tròn
            colors = ['#4CAF50', '#2196F3', '#FFC107', '#F44336']
            plt.figure(figsize=(8, 6))
            _, _, autotexts = plt.pie(
                values,
                labels=labels,
                autopct='%1.1f%%',
                startangle=90,
                colors=colors[:len(labels)],
                textprops={'fontsize': 12, 'weight': 'bold'}
            )

            # Làm nổi bật phần trăm
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontsize(14)

            plt.title('Biểu đồ xếp loại học lực',
                      fontsize=16,
                      weight='bold',
                      pad=20)
            plt.axis('equal')

            # Thêm chú thích với số lượng
            legendLabels = [f'{label}: {value} SV' for label,
                            value in zip(labels, values)]
            plt.legend(legendLabels,
                       loc='best',
                       fontsize=11,
                       bbox_to_anchor=(1.0, 0.5))

            plt.tight_layout()
            plt.show()
            print("Đã hiển thị biểu đồ tròn!")

        case '2':
            # Vẽ biểu đồ cột
            colors = ['#4CAF50', '#2196F3', '#FFC107', '#F44336']
            plt.figure(figsize=(10, 6))
            bars = plt.bar(labels, values, color=colors[:len(
                labels)], alpha=0.8, edgecolor='black')

            # Thêm giá trị lên đầu mỗi cột
            for bar in bars:
                height = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2., height,
                         f'{int(height)}',
                         ha='center', va='bottom',
                         fontsize=12, weight='bold')

            plt.xlabel('Xếp loại', fontsize=13, weight='bold')
            plt.ylabel('Số lượng sinh viên', fontsize=13, weight='bold')
            plt.title('Biểu đồ xếp loại học lực',
                      fontsize=16,
                      weight='bold',
                      pad=20)
            plt.grid(axis='y', alpha=0.3, linestyle='--')
            plt.ylim(0, max(values) * 1.15)

            plt.tight_layout()
            plt.show()
            print("Đã hiển thị biểu đồ cột!")

        case _:
            print("Lựa chọn không hợp lệ!")


def exportToCsv():
    """
    Xuất toàn bộ danh sách sinh viên ra file CSV.
    """
    print("\n--- LƯU VÀO FILE CSV ---")
    saveToCsv()


def displayMenu():
    """
    Hiển thị menu chính của chương trình.
    """
    print("----- Menu chương trình Quản lý Sinh viên -----")
    print("1.  Hiển thị danh sách sinh viên")
    print("2.  Thêm mới sinh viên")
    print("3.  Cập nhật thông tin sinh viên")
    print("4.  Xóa sinh viên")
    print("5.  Tìm kiếm sinh viên")
    print("6.  Sắp xếp danh sách sinh viên")
    print("7.  Thống kê điểm TB")
    print("8.  Vẽ biểu đồ thống kê")
    print("9.  Lưu vào file CSV")
    print("10. Thoát")


def handleMenuChoice(choice: str) -> bool:
    """
    Xử lý lựa chọn từ menu chính.

    Args:
        choice: Lựa chọn của người dùng (string từ '1' đến '10')

    Returns:
        True nếu tiếp tục chương trình, False nếu muốn thoát
    """
    match choice:
        case '1':
            displayAllStudents()
        case '2':
            addStudent()
        case '3':
            updateStudent()
        case '4':
            deleteStudent()
        case '5':
            searchStudent()
        case '6':
            sortStudents()
        case '7':
            displayStatistics()
        case '8':
            displayChart()
        case '9':
            exportToCsv()
        case '10':
            print("\nĐang lưu dữ liệu...")
            saveToJson()
            print("Hẹn gặp lại!")
            return False
        case _:
            print("\nLựa chọn không hợp lệ! Vui lòng chọn từ 1-10.")

    return True


def main():
    """Hàm chính điều khiển chương trình."""
    print("Hệ thống quản lý sinh viên")

    # Tải dữ liệu từ file khi khởi động
    loadData()

    while True:
        displayMenu()
        choice = input("Nhập lựa chọn của bạn (1-10): ").strip()

        # Xử lý lựa chọn bằng match-case
        should_continue = handleMenuChoice(choice)
        if not should_continue:
            break

        input("\nNhấn Enter để tiếp tục...")


# Chạy chương trình
if __name__ == "__main__":
    main()