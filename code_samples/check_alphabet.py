# объявление функции
def is_pangram(text):
    alphabet = [chr(i) for i in range(97, 123)]
    text = text.lower()
    for i in range(len(alphabet)):
        if alphabet[i] in text:
            continue
        else:
            return False
    else:
        return True


# считываем данные
text = input()
# вызываем функцию
print(is_pangram(text))
