a = int(input("Nhập vào 1 số nguyên a: "))
b = int(input("Nhập vào 1 số nguyên b: "))

if a > b: 
    a, b = b, a     
found_primes = False
for n in range(a, b + 1):
    if n <= 1:
        continue
    is_prime = True

    i = 2
    while i * i <= n:
        if n % i == 0:
            is_prime = False
            break  
        i += 1
        
    if is_prime:
        print(n, end=" ")
        found_primes = True
        
if not found_primes:
    print("Không có số nguyên tố nào trong khoảng này.", end="")
    