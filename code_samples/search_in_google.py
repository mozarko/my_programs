n = int(input())

letters = []
search = []

for _ in range(n):
    s = input()
    letters.append(s)
k = int(input())

for _ in range(k):
    f = input()
    search.append(f)

for i in range(len(search)):
    j = 0
    while j < len(letters):
        if search[i].casefold() not in letters[j].casefold():
            del letters[j]
            j = -1
        j += 1

print(*letters, sep='\n')
