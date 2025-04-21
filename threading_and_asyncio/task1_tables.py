from task1_data import Questions, Students, Results, Examiners


def print_results(examiners_list, students_list, elapsed_time):
    print("\033[H\033[J")
    print(table_student_finish())
    print(table_examiners_finish(Examiners.examiners_list))

    # Время с момента начала экзамена и до момента его завершения
    print(f"Время с момента начала экзамена и до момента его завершения: {elapsed_time:.2f}")

    # Имена лучших студентов
    best_students = [student.name for student in students_list if student.status == "Сдал"]
    print(f"Имена лучших студентов: {', '.join(best_students)}")

    # Имена лучших экзаменаторов
    best_examiners = [examiner.name for examiner in examiners_list if examiner.failed_students == 0]
    print(f"Имена лучших экзаменаторов: {', '.join(best_examiners)}")

    # Имена студентов, которых после экзамена отчислят
    expelled_students = [student.name for student in students_list if student.status == "Провалил"]
    print(f"Имена студентов, которых после экзамена отчислят: {', '.join(expelled_students)}")

    # Лучшие вопросы
    max_count = max(best_q.count for best_q in Results.best_dict.values())
    count_best_quest = 0
    print("Лучшие вопросы: ", end="")
    for best_q in Results.best_dict.values():
        if best_q.count == max_count:
            count_best_quest += 1
    for best_q in Results.best_dict.values():
        if best_q.count == max_count:
            print(' '.join(best_q.name), end="")
            count_best_quest -= 1
            if count_best_quest > 0:
                print(", ", end="")
    print()
    # Вывод: экзамен не удался
    count_student_fail = 0
    count_student_total = 0
    for examiner in examiners_list:
        count_student_fail += examiner.failed_students
        count_student_total += examiner.total_students
    percent = (count_student_total - count_student_fail) / count_student_total
    if percent >= 0.85:
        print("Вывод: Экзамен удался")
    else:
        print(f"Вывод: экзамен не удался")
    #print(f"Сдали экзамен {count_student_total - count_student_fail}\n"
    #      f"Всего студентов {count_student_total}\n"
    #      f"Процент {percent:.2f}")


def table_student():
    data = [[student.name, student.status, student.correct_answers] for student in
            Students.students_list]

    # Заголовки столбцов
    headers = ["Студент", "Статус", "Правильных ответов"]

    # Определяем максимальную длину для каждого столбца
    max_lens = [max(len(str(row[i])) for row in data + [headers]) + 2 for i in range(len(headers))]

    # Функция для создания строки таблицы
    def create_row(cells, max_lens):
        return "| " + " | ".join(str(cell).ljust(max_len) for cell, max_len in zip(cells, max_lens)) + " |"

    # Создаем верхнюю границу таблицы
    def create_border(max_lens):
        return "+-" + "-+-".join("-" * max_len for max_len in max_lens) + "-+"

    # Создаем таблицу
    border = create_border(max_lens)
    table = [border]
    table.append(create_row(headers, max_lens))
    table.append(border)

    for row in data:
        table.append(create_row(row, max_lens))
    table.append(border)

    # Возвращаем таблицу как строку
    return "\n".join(table)

def table_student_finish():
    data_for_sort = [[student.name, student.status] for student in
            Students.students_list]
    sorted_data = sorted(data_for_sort, key=lambda x: x[1] != "Сдал")
    data = sorted_data

    # Заголовки столбцов
    headers = ["Студент", "Статус"]

    # Определяем максимальную длину для каждого столбца
    max_lens = [max(len(str(row[i])) for row in data + [headers]) + 2 for i in range(len(headers))]

    # Функция для создания строки таблицы
    def create_row(cells, max_lens):
        return "| " + " | ".join(str(cell).ljust(max_len) for cell, max_len in zip(cells, max_lens)) + " |"

    # Создаем верхнюю границу таблицы
    def create_border(max_lens):
        return "+-" + "-+-".join("-" * max_len for max_len in max_lens) + "-+"

    # Создаем таблицу
    border = create_border(max_lens)
    table = [border]
    table.append(create_row(headers, max_lens))
    table.append(border)

    for row in data:
        table.append(create_row(row, max_lens))
    table.append(border)

    # Возвращаем таблицу как строку
    return "\n".join(table)


def table_examiners(examiners_list):
    data = [
        [
            examiner.name,
            examiner.current_student,
            examiner.total_students,
            examiner.failed_students,
            f"{examiner.work_time:.2f}",
            examiner.mood
        ]
        for examiner in examiners_list
    ]
    headers = ["Экзаменатор", "Текущий студент", "Всего студентов", "Завалил", "Время работы", "Настроение"]
    max_lens = [max(len(str(row[i])) for row in data + [headers]) + 2 for i in range(len(headers))]

    # Функция для создания строки таблицы
    def create_row(cells, max_lens):
        return "| " + " | ".join(str(cell).ljust(max_len) for cell, max_len in zip(cells, max_lens)) + " |"

    # Создаем верхнюю границу таблицы
    def create_border(max_lens):
        return "+-" + "-+-".join("-" * max_len for max_len in max_lens) + "-+"

    # Создаем таблицу
    border = create_border(max_lens)
    table = [border]
    table.append(create_row(headers, max_lens))
    table.append(border)

    for row in data:
        table.append(create_row(row, max_lens))
    table.append(border)

    # Возвращаем таблицу как строку
    return "\n".join(table)

def table_examiners_finish(examiners_list):
    data = [
        [
            examiner.name,
            examiner.total_students,
            examiner.failed_students,
            f"{examiner.work_time:.2f}",
        ]
        for examiner in examiners_list
    ]
    headers = ["Экзаменатор", "Всего студентов", "Завалил", "Время работы"]
    max_lens = [max(len(str(row[i])) for row in data + [headers]) + 2 for i in range(len(headers))]

    # Функция для создания строки таблицы
    def create_row(cells, max_lens):
        return "| " + " | ".join(str(cell).ljust(max_len) for cell, max_len in zip(cells, max_lens)) + " |"

    # Создаем верхнюю границу таблицы
    def create_border(max_lens):
        return "+-" + "-+-".join("-" * max_len for max_len in max_lens) + "-+"

    # Создаем таблицу
    border = create_border(max_lens)
    table = [border]
    table.append(create_row(headers, max_lens))
    table.append(border)

    for row in data:
        table.append(create_row(row, max_lens))
    table.append(border)

    # Возвращаем таблицу как строку
    return "\n".join(table)