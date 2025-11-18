a, b, c = map(float, input("Nhập vào 3 cạnh a, b, c: ").split())

if a > 0 and b > 0 and c > 0 and (a + b > c) and (a + c > b) and (b + c > a):
    print("Là 1 tam giác")
else:
    print("Không phải là 1 tam giác")
