n = int(input("Total numbers you want to enter: "))
numbers = []

for i in range(1, n + 1):
    num = int(input(f"Enter number {i}: "))
    numbers.append(num)
numbers.sort()
print("sorted list:", numbers)
print("The second largest number is:", numbers[-2])