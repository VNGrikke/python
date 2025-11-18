N = int(input("Nhập vào 1 số nguyên N: "))

if N < 1:
    print("Không thể tính tổng nếu N < 1")
else:
    total = 0
    for i in range(1, N + 1):
        total += i
    print(f"Tổng các số từ 1 đến {N} là: {total}")
