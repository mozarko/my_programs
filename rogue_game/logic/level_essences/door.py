from __future__ import annotations
from random import choice

class Door:
    def __init__(self, color_idx: int, coridors: list[Corridor]):
        """
        Случайным образом выбирается коридор в котором будет находиться дверь.

        Args:
            color_idx int: Цвет двери.
            coridors list[Corridor]: Список лабиринта из номеров комнат.
        """
        self.color_idx = color_idx
        self.corridor  = choice(coridors)
        self.corridor.color_idx = self.color_idx
