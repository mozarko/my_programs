from __future__ import annotations
import random

class Room:
    def __init__(self, x: int, y: int, w: int, h: int, room_number: int):
        """
        Инициализация обьекта класса комнаты.

        Args:
            x (int): Координата по оси Х левого верхнего угла комнаты.
            y (int): Координата по оси Y левого верхнего угла комнаты.
            w (int): Ширина комнаты.
            h (int): Длинна комнаты.
        """
        self.x1 = x
        self.y1 = y
        self.x2 = x + w - 1
        self.y2 = y + h - 1
        self.room_number = room_number

    def get_center(self) -> [int, int]:
        """
        Нахождение центра комнаты.
        Returns:
            [int, int]: Координаты х и у центра комнаты.
        """
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return center_x, center_y

    def is_intersect(self, other: Room):
        return (self.x1 <= other.x2 and self.x2 >= other.x1
                and self.y1 <= other.y2 and self.y2 >= other.y1)

    def generate_exit(self)-> [int, int]:
        """
        Задает случайным образом координаты окончания уровня в комнате.
        Returns:
            [int, int]: Координаты х и у точки выхода из уровня.
        """
        x = random.randint(self.x1 + 1, self.x2 - 1)
        y = random.randint(self.y1 + 1, self.y2 - 1)
        return x, y

    def is_room(self, x: int, y: int) -> bool:
        """
        Проверяет, находится ли точка с координатами (x, y) внутри комнаты.
        Args:
            x (int): Координата x точки.
            y (int): Координата y точки.
        Returns:
            bool: True, если точка находится внутри комнаты, иначе False.
        """
        return self.x1 <= x <= self.x2 and self.y1 <= y <= self.y2
            