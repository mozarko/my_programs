n = int(input())

numbers = []

for _ in range(n):
    number = int(input())
    if number not in numbers:
        numbers.append(number)

print(len(numbers), end="")
