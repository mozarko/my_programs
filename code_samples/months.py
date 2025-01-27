# объявление функции
def get_month(language, number):
    month_ru = ["ничего", "январь", "февраль", "март", "апрель", "май", "июнь", "июль", "август", "сентябрь", "октябрь",
                "ноябрь",
                "декабрь"]
    month_eng = ['nothing', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september',
                 'october',
                 'november', 'december']

    if language == 'ru':
        return month_ru[number]
    if language == 'en':
        return month_eng[number]


# считываем данные
lan = input()
num = int(input())

# вызываем функцию
print(get_month(lan, num))
