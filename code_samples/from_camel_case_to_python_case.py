# объявление функции
def convert_to_python_case(text):
    list = []
    j = 0
    for i in range(1, len(text)):
        if text[i].isupper():
            list.append(text[j:i])
            j = i
    for i in range(1, len(text)):
        if text[-i].isupper():
            list.append(text[-i:])
            break
    text_new = '_'.join(list)
    text_new = text_new.lower()
    return text_new


# считываем данные
txt = input()

# вызываем функцию
print(convert_to_python_case(txt))
