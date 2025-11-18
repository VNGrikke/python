a = int(input("Nhập vào 1 số nguyên a: "))
b = int(input("Nhập vào 1 số nguyên b: "))

start = a if a % 2 == 0 else a + 1
array = list(range(start, b + 1, 2))
print(array)
