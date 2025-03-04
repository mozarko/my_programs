from __future__ import annotations
from random import randint, choice


class Key:
    def __init__(self, color_idx: int, rooms: list[Room]):
        """
        Случайным образом выбирается комната в которой будет находиться ключ.

        Args:
            color_idx int: Цвет ключа.
            rooms list[Room]: Список комнат для выбора размещения ключа.
        """
        self.symb = '&'
        self.color_idx = color_idx
        self.room = choice(rooms)
        self.coordinates = self.set_coordinates()

    def set_coordinates(self):
        """
        Случайным образом выбирается точка размещения ключа в комнате.

        Returns:
            list[int]: Координаты размещения ключа.
        """
        return [randint(self.room.x1, self.room.x2), randint(self.room.y1, self.room.y2)]
