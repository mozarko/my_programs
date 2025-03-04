from __future__ import annotations
from abc import ABC, abstractmethod
import random
import math

from constants.game_constants import *


class MovementStrategy(ABC):
    @abstractmethod
    def move(self, entity, level):
        """Moves an entity (character or enemy) based on strategy."""
        pass


class PlayerMovementStrategy(MovementStrategy):
    def move(self, player, level, direction):
        dx, dy = DIRECTION_MAP[direction]
        if not level.is_blocked(player.x + dx, player.y + dy):
            player.x += dx
            player.y += dy
            player.stats.tiles_walked += 1
            player.remove_buff()


class PlayerMovementStrategy3D(MovementStrategy):
    def __init__(self, player_speed=1, rotation_speed=0.1):
        self.player_angle = 0
        self.player_speed = player_speed
        self.rotation_speed = rotation_speed

    def move(self, player, level, char):
        # Пересчитываем синус и косинус угла
        sin_a = math.sin(self.player_angle)
        cos_a = math.cos(self.player_angle)

        # Движение вперед и назад
        if char == 'w':
            new_x = player.x + self.player_speed * cos_a
            new_y = player.y + self.player_speed * sin_a
            player.stats.tiles_walked += 1
            player.remove_buff()
        elif char == 's':
            new_x = player.x - self.player_speed * cos_a
            new_y = player.y - self.player_speed * sin_a
            player.stats.tiles_walked += 1
            player.remove_buff()
        else:
            new_x, new_y = player.x, player.y

        # Проверка границ уровня
        try:
            is_blocked = level.is_blocked(int(round(new_x)), int(round(new_y)))
        except:
            is_blocked = True

        if not is_blocked:
            player.x = int(round(new_x))
            player.y = int(round(new_y))

        # Повороты
        if char == 'a':
            self.player_angle -= self.rotation_speed
        elif char == 'd':
            self.player_angle += self.rotation_speed

        # Нормализация угла
        self.player_angle %= 2 * math.pi


class BasicMovementStrategy(MovementStrategy):
    def move(self, enemy, level, player_x, player_y):
        if abs(enemy.x - player_x) <= enemy.hostility and abs(enemy.y - player_y) <= enemy.hostility:
            if player_x > enemy.x and not level.is_blocked(enemy.x + 1, enemy.y):
                enemy.x += 1
            elif player_x < enemy.x and not level.is_blocked(enemy.x - 1, enemy.y):
                enemy.x -= 1
            if player_y > enemy.y and not level.is_blocked(enemy.x, enemy.y + 1):
                enemy.y += 1
            elif player_y < enemy.y and not level.is_blocked(enemy.x, enemy.y - 1):
                enemy.y -= 1


class GhostMovementStrategy(MovementStrategy):
    def move(self, enemy, level, player_x, player_y):
        if abs(enemy.x - player_x) <= enemy.hostility and abs(enemy.y - player_y) <= enemy.hostility:
            for _ in range(3):
                dx = random.randint(-3, 3)
                dy = random.randint(-3, 3)

                new_x = enemy.x + dx
                new_y = enemy.y + dy

                if 0 <= new_x < MAP_WIDTH and 0 <= new_y < MAP_HEIGHT and not level.is_blocked(new_x, new_y):
                    enemy.x = new_x
                    enemy.y = new_y
                    break


class OgreMovementStrategy(MovementStrategy):
    def move(self, enemy, level, player_x, player_y):
        if abs(enemy.x - player_x) <= enemy.hostility and abs(enemy.y - player_y) <= enemy.hostility:
            if player_x > enemy.x and not level.is_blocked(enemy.x + 2, enemy.y):
                enemy.x += 2
            elif player_x < enemy.x and not level.is_blocked(enemy.x - 2, enemy.y):
                enemy.x -= 2
            if player_y > enemy.y and not level.is_blocked(enemy.x, enemy.y + 2):
                enemy.y += 2
            elif player_y < enemy.y and not level.is_blocked(enemy.x, enemy.y - 2):
                enemy.y -= 2


class SnakeMovementStrategy(MovementStrategy):
    def __init__(self):
        self.direction = 1

    def move(self, enemy, level, player_x, player_y):
        if abs(enemy.x - player_x) <= enemy.hostility and abs(enemy.y - player_y) <= enemy.hostility:
            if player_x > enemy.x and not level.is_blocked(enemy.x + 1, enemy.y - self.direction):
                enemy.x += 1
                enemy.y -= self.direction
            elif player_x < enemy.x and not level.is_blocked(enemy.x - 1, enemy.y + self.direction):
                enemy.x -= 1
                enemy.y += self.direction
            if player_y > enemy.y and not level.is_blocked(enemy.x - self.direction, enemy.y + 1):
                enemy.y += 1
                enemy.x -= self.direction
            elif player_y < enemy.y and not level.is_blocked(enemy.x + self.direction, enemy.y - 1):
                enemy.y -= 1
                enemy.x += self.direction

            self.direction *= -1
