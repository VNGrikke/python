N = int(input("Nhập vào 1 số nguyên N: "))

if N < 0:
    print("Không thể tính tích cho số âm")
else:
    product = 1
    for i in range(1, N + 1):
        product *= i
    print(f"Tích các số từ 1 đến {N} là: {product}")
