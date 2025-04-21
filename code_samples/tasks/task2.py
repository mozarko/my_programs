number = int(input())

if number >= 0 and number <= 9:
    print("True")
    exit(0)

number_list = []

while (number != 0):
    x = number % 10
    number_list.append(x)
    number = number // 10

for i in range(int(len(number_list) / 2)):
    if number_list[i] != number_list[len(number_list) - 1 - i]:
        print("False", end="")
        exit(0)

print("True", end="")
exit(0)
