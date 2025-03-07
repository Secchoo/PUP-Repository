def prog01():
    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))
    print(f"The bigger number is: {max(num1, num2)}")

def prog02():
    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))
    print("Equal") if num1 == num2 else print("Not Equal")

def prog03():
    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))
    print(f"The sum is: {num1 + num2}")

def prog04():
    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))
    print(f"The product is: {num1 * num2}")

def prog05():
    num1 = float(input("Enter dividend: "))
    num2 = float(input("Enter divisor: "))
    if num2 != 0:
        print(f"The quotient is: {num1 / num2}")
    else:
        print("Error: Division by zero!")

def prog06():
    num1 = float(input("Enter base number: "))
    num2 = float(input("Enter exponent: "))
    print(f"{num1} raised to {num2} is: {pow(num1, num2)}")

def prog07():
    total_sum = 0
    for i in range(10):
        num = float(input(f"Enter number {i+1}: "))
        total_sum += num
    print(f"The sum of all numbers is: {total_sum}")

def prog08():
    odd_count = 0
    for i in range(10):
        num = int(input(f"Enter number {i+1}: "))
        if num % 2 != 0:
            odd_count += 1
    print(f"Number of odd numbers: {odd_count}")

def prog09():
    for i in range(51):
        print(i*2, end=' ')
    print()

def prog10():
    for i in range(101):
        if i % 10 != 0:
            print(i, end=' ')
    print()

def main():
    while True:
        print("\n=== Number Processing Programs ===")
        print("1. Find bigger number")
        print("2. Check if numbers are equal")
        print("3. Calculate sum")
        print("4. Calculate product")
        print("5. Calculate quotient")
        print("6. Calculate power")
        print("7. Sum of ten numbers")
        print("8. Count odd numbers")
        print("9. Print even numbers 0-100")
        print("10. Print numbers not ending in zero")
        print("0. Exit")
        
        choice = input("\nEnter your choice (0-10): ")
        
        if choice == '0':
            print("Goodbye!")
            break
        elif choice == '1':
            prog01()
        elif choice == '2':
            prog02()
        elif choice == '3':
            prog03()
        elif choice == '4':
            prog04()
        elif choice == '5':
            prog05()
        elif choice == '6':
            prog06()
        elif choice == '7':
            prog07()
        elif choice == '8':
            prog08()
        elif choice == '9':
            prog09()
        elif choice == '10':
            prog10()
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()