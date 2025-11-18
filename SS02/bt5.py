number = input("Nhap vao mot so nguyen: ")


reNumber = "".join(reversed(number))

if number == reNumber:
    print(f"{number} là số đối xứng")
else:
    print(f"{number} ko phải số đối xứng")
