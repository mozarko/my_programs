from __future__ import annotations
from random import randint

from logic.level_essences.room import Room


class Corridor:
    def __init__(self):
        self.rooms = []
        self.coordinates = []
        self.color_idx = 8

    def connect_vertical_rooms(self, room1: Room, room2: Room):
        """
        Генерирует коридор, соединяя две комнаты по вертикали.

        Args:
            room1 (Room): Первая из двух комнат, между которыми генерируется коридор.
            room2 (Room): Вторая из двух комнат, между которыми генерируется коридор.
        """
        self.rooms = [room1, room2]
        r1x1 = room1.x1
        r1y1 = room1.y1
        r1x2 = room1.x2
        r1y2 = room1.y2
        r2x1 = room2.x1
        r2y1 = room2.y1
        r2x2 = room2.x2
        r2y2 = room2.y2

        # Условие при котором между комнатами можно провести вертикальный коридор
        if r1x1 + 1 < r2x2 and r1x2 > r2x1 + 1:
            x_rand = randint(max(r1x1, r2x1) + 1, min(r1x2, r2x2) - 1)
            self.create_vertical_tunnel(x_rand, r1y2, r2y1)

            # Условие при котором нижняя комната находится левее верхней и вертикальный коридор невозможен
        elif r1x1 > r2x1 + 2:
            x_rand = randint(r2x1 + 1, min(r1x1 - 2, r2x2 - 1))
            y_rand = randint(r1y1 + 1, r1y2 - 1)
            self.create_corridor_type_a(r1x1, y_rand, x_rand, r2y1)

            # Условие при котором нижняя комната находится правее верхней и вертикальный коридор невозможен
        elif r2x1 > r1x1 + 2:
            x_rand = randint(r1x1 + 1, min(r2x1 - 2, r1x2 - 1))
            y_rand = randint(r2y1 + 1, r2y2 - 1)
            self.create_corridor_type_a(r2x1, y_rand, x_rand, r1y2)

    def connect_horizontal_rooms(self, room1: Room, room2: Room):
        """
        Генерирует коридор, соединяя две комнаты по горизонтали.

        Args:
            room1 (Room): Первая из двух комнат, между которыми генерируется коридор.
            room2 (Room): Вторая из двух комнат, между которыми генерируется коридор.
        """
        self.rooms = [room1, room2]
        r1x1 = room1.x1
        r1y1 = room1.y1
        r1x2 = room1.x2
        r1y2 = room1.y2
        r2x1 = room2.x1
        r2y1 = room2.y1
        r2x2 = room2.x2
        r2y2 = room2.y2

        # Условие при котором между комнатами можно провести горизонтальный коридор
        if r1y2 > r2y1 + 1 and r1y1 + 1 < r2y2:
            y_rand = randint(max(r1y1, r2y1) + 1, min(r1y2, r2y2) - 1)
            self.create_horizontal_tunnel(r1x2, r2x1, y_rand)

            # Условие при котором правая комната находится выше левой и горизонтальный коридор невозможен
        elif r1y1 > r2y1 + 2:
            x_rand = randint(r1x1+1, r1x2-1)
            y_rand = randint(r2y1+1, min(r2y2-1, r1y1-2))
            self.create_corridor_type_a(r2x1, y_rand, x_rand, r1y1)

            # Условие при котором правая комната находится ниже левой и горизонтальный коридор невозможен
        elif r2y1 > r1y1 + 2:
            x_rand = randint(r2x1+1, r2x2-1)
            y_rand = randint(r1y1+1, min(r1y2-1, r2y1-2))
            self.create_corridor_type_a(r1x2, y_rand, x_rand, r2y1)

    def create_vertical_tunnel(self, x: int, y1: int, y2: int):
        """
        Генерирует горизонтальную линию коридора.

        Args:
            x (int): Координата по горизонтали для линии коридора.
            y1 (int): Координата по вертикали для начала линии коридора.
            y2 (int): Координата по вертикали для конца линии коридора.
        """
        for i in range(y1+1, y2):
            self.coordinates.append([x, i])

    def create_horizontal_tunnel(self, x1: int, x2: int, y: int):
        """
        Генерирует горизонтальную линию коридора.

        Args:
            x1 (int): Координата по горизонтали для начала линии коридора.
            x2 (int): Координата по горизонтали для конца линии коридора.
            y (int): Координата по вертикали для линии коридора.
        """
        for i in range(x1+1, x2):
            self.coordinates.append([i, y])

    def create_corridor_type_a(self, x1: int, y1: int, x2: int, y2: int):
        """
        Генерирует коридор с изгибом.

        Args:
            x1 (int): Начальная координата по оси Х коридора с изгибом.
            y1 (int): Начальная координата по оси Y коридора с изгибом.
            x2 (int): Конечная координата по оси Х коридора с изгибом.
            y2 (int): Конечная координата по оси Y коридора с изгибом.
        """
        self.create_vertical_tunnel(x2, min(y1, y2), max(y1, y2))
        self.coordinates.append([x2, y1])
        self.create_horizontal_tunnel(min(x1, x2), max(x1, x2), y1)
