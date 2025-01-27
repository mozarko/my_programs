from random import choices, randint, uniform


class Examiners:
    examiners_list = []

    moods = ["плохое", "хорошее", "нейтральное"]
    probabilities = [1 / 8, 1 / 4, 5 / 8]

    def __init__(self, name, gender):
        self.answers_list = []
        self.name = name
        self.gender = gender
        self.lunch = False
        self.mood = choices(self.moods, self.probabilities)[0]
        self.exam_time = round(uniform(len(name) - 1, len(name) + 1), 2)
        self.work_time = 0
        self.examiners_list.append(self)
        self.current_student = "-"  # Текущий студент
        self.total_students = 0  # Всего студентов
        self.failed_students = 0  # Завалил студентов
        self.answer = "Пусто"


class Students:
    students_list = []
    best_student = ""

    def __init__(self, name, gender):
        self.name = name
        self.gender = gender
        self.status = "Очередь"
        self.answer = "Пусто"
        self.correct_answers = 0
        self.students_list.append(self)


class Questions:
    tickets = []

    def __init__(self, questions_list):
        self.questions_list = questions_list  # Список вопросов
        self.tickets.append(self)

    def __getitem__(self, index):
        # Этот метод позволяет обращаться к элементам списка по индексу
        return self.questions_list[index]

    def __len__(self):
        # Этот метод позволяет узнать длину списка
        return len(self.questions_list)

    def __repr__(self):
        return f"{self.questions_list}"


class Results:
    best_dict = {}  # Словарь для хранения объектов

    def __init__(self, name=""):
        self.name = name
        self.count = 1

    @classmethod
    def get_or_create(cls, name):
        if name not in cls.best_dict:
            # Создаем новый объект и добавляем в словарь
            cls.best_dict[name] = cls(name)
        else:
            # Увеличиваем счетчик для существующего объекта
            cls.best_dict[name].count += 1
        return cls.best_dict[name]


def load_questions(file):
    try:
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                parts = line.split(" ")
                res = []
                if len(parts) >= 3:
                    res.append(parts[0])
                    res.append(parts[1])
                    res.append(' '.join(parts[2:]))
                    Questions(res)
                else:
                    print("Файл с вопросами неверного формата")
                    exit(1)
    except FileNotFoundError:
        print(f"Файл {file} не найден.")
        exit(1)


def load_students(file):
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            parts = line.split(" ")
            name = parts[0]
            gender = parts[1]
            Students(name, gender)


def load_examiners(file):
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            parts = line.split(" ")
            name = parts[0]
            gender = parts[1]
            Examiners(name, gender)
