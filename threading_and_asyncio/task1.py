from random import random, uniform, choices, sample
import threading
import time
import os
from task1_data import Examiners, Students, Questions, Results, load_questions, load_students, load_examiners
from task1_tables import print_results, table_student, table_examiners


# Функция для сдачи экзамена
def pass_exam(student, examiner, tickets):
    time.sleep(examiner.exam_time)
    questions_prob_man = [1 / 2, 1 / 3, 1 / 6]
    questions_prob_woman = [1 / 6, 1 / 3, 1 / 2]
    tickets_for_exam = sample(tickets, 3)
    students_answers = []
    correct_answers = []

    for ticket in tickets_for_exam:
        student.answer = choices(ticket, questions_prob_man if examiner.gender == "М" else questions_prob_woman)[0]
        students_answers.append(student.answer)
        Results.get_or_create(ticket)
    for ticket in tickets_for_exam:
        examiner.answer = choices(ticket, questions_prob_man if examiner.gender == "М" else questions_prob_woman)[0]
        correct_answers.append(examiner.answer)
        examiner.answers_list.append([examiner.answer, student.name])
        while True:
            if random() < 1 / 3:
                for answer in ticket:
                    if answer not in correct_answers:
                        examiner.answer = answer
                        correct_answers.append(examiner.answer)
                        examiner.answers_list.append([examiner.answer, student.name])
                        break
            else:
                break
    for answer in students_answers:
        if answer in correct_answers:
            student.correct_answers += 1
    time.sleep(1)
    check_exam(student, examiner)


def check_exam(student, examiner):
    if examiner.mood == "плохое":
        student.status = "Провалил"
        examiner.failed_students += 1
        return
    if examiner.mood == "хорошее":
        student.status = "Сдал"

    if examiner.mood == "нейтральное":
        if student.correct_answers >= 2:
            student.status = "Сдал"
        else:
            student.status = "Провалил"
            examiner.failed_students += 1


# Функция для обновления данных в таблице
def update_table(examiner, students_list, tickets, start_time):
    exam = True
    while exam:
        time.sleep(uniform(1, 3))
        # Ищем студента со статусом "Очередь"
        student = next((s for s in students_list if s.status == "Очередь"), None)
        if student:
            examiner.current_student = student.name
            examiner.total_students += 1
            student.status = "Сдает"
            pass_exam(student, examiner, tickets)
            examiner.work_time = time.time() - start_time
            student_next = next((s for s in students_list if s.status == "Очередь"), None)
            if examiner.work_time > 10 and examiner.lunch == False and student_next:
                examiner.lunch = True
                examiner.current_student = "\"На обеде\""
                time.sleep(uniform(12, 18))
            examiner.work_time = time.time() - start_time
        else:
            # Если нет студентов в очереди, завершаем работу
            examiner.current_student = "-"
            examiner.work_time = time.time() - start_time
            exam = False
    time.sleep(1)


# Функция для отображения обеих таблиц
def display_tables(examiners_list, students_list, lock, stop_event, start_time, delay):
    while not stop_event.is_set():
        with lock:
            count_students_in_queue = len([s for s in students_list if s.status == "Очередь"])
            elapsed_time = time.time() - start_time
            # Очищаем экран (для удобства отображения)
            print("\033[H\033[J")

            # Выводим таблицу студентов
            print(table_student())

            # Выводим таблицу экзаменаторов
            print(table_examiners(examiners_list))

            print(f"Осталось студентов в очереди: {count_students_in_queue}")

            # Выводим время работы программы
            print(f"Время работы программы: {elapsed_time:.2f} секунд")
            print(f"Обновление: {delay}")

        time.sleep(delay)  # Обновляем таблицу

    # Обновляем таблицы один последний раз после завершения всех потоков
    with lock:
        print("\033[H\033[J")
        print(table_student())
        print(table_examiners(examiners_list))


# Основная функция
def main():
    delay = 0.1
    if 'linux' in os.uname().sysname.lower():
        delay = 0.01

    start_time = time.time()  # Засекаем время начала работы
    load_examiners("examiners.txt")
    load_students("students.txt")
    load_questions("questions.txt")

    lock = threading.Lock()  # Мьютекс для синхронизации доступа к очереди
    stop_event = threading.Event()  # Событие для остановки потоков

    # Создаем потоки для каждого экзаменатора
    examiner_threads = []
    for examiner in Examiners.examiners_list:
        thread = threading.Thread(target=update_table,
                                  args=(examiner, Students.students_list, Questions.tickets, start_time))
        examiner_threads.append(thread)
        thread.start()

    # Создаем поток для отображения таблиц
    display_thread = threading.Thread(target=display_tables, args=(
        Examiners.examiners_list, Students.students_list, lock, stop_event, start_time, delay))
    display_thread.start()

    # Ждем завершения потоков экзаменаторов
    for thread in examiner_threads:
        thread.join()

    stop_event.set()

    # Останавливаем поток отображения таблиц
    display_thread.join()

    elapsed_time = time.time() - start_time
    # Выводим результаты после завершения экзамена
    print_results(Examiners.examiners_list, Students.students_list, elapsed_time)

if __name__ == "__main__":
    main()
