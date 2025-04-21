pets = [s for s in input().split()]

result = {}
for letter in pets:
    result[letter] = result.get(letter, -1) + 1
    if result[letter] > 0:
        print(letter + '_' + str(result[letter]), end=' ')
    else:
        print(letter, end=' ')
