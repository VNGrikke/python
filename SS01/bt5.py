inp = input("Enter something: ")
if inp in ("0", "1"):
    print("You entered:", bool(int(inp)))
else:
    print("Invalid input! Please enter 0 or 1.")