def merge(values):  # values - это список словарей
    result = {}
    for dict in values:
        for key, value in dict.items():
            result.setdefault(key, set()).add(value)
    return result


print(merge([{'a': 1, 'b': 2}, {'b': 10, 'c': 100}, {'a': 1, 'b': 17, 'c': 50}, {'a': 5, 'd': 777}]))

