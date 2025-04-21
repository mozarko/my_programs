words = ['hello', 'bye', 'yes', 'no', 'python', 'apple', 'maybe', 'stepik', 'beegeek']


result = {i: [ord(i[j]) for j in range(len(i))] for i in words}

print(result)
