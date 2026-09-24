def add(a, b):
    return a + b

def sub(a, b):
    return a - b

def mult(a, b):
    return a * b

def div(a, b):
    return a / b


while True:
    print("\n1 Add")
    print("2 Subtract")
    print("3 Multiply")
    print("4 Divide")
    print("5 Exit")

    choice = input("Choose: ")

    if choice == "5":
        break

    num1 = int(input("First number: "))
    num2 = int(input("Second number: "))

    if choice == "1":
        print(add(num1, num2))
    elif choice == "2":
        print(sub(num1, num2))
    elif choice == "3":
        print(mult(num1, num2))
    elif choice == "4":
        print(div(num1, num2))