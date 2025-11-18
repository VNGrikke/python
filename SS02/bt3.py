number = int(input("Nhập vào 1 số nguyên: "))

if number % 3 == 0 and number % 5 == 0:
    print(f"{number} là số chia hết cho cả 3 và 5")
elif number % 3 == 0:
    print(f"{number} là số chia hết cho 3")
elif number % 5 == 0:
    print(f"{number} là số chia hết cho 5")
else:
    print(f"{number} không phải là số chia hết cho cả 3 và 5")
