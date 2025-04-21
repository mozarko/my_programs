import json
from constants.game_constants import *


class Stats:
    def __init__(self):
        self.gold = 0
        self.eaten_food = 0
        self.used_elixir = 0
        self.used_scrolls = 0
        self.enemies_defeated = 0
        self.hits_dealt = 0
        self.hits_taken = 0
        self.tiles_walked = 0

    @staticmethod
    def save_stats(statistics: list[dict]):
        """Сохраняет обновленную статистику в JSON-файл."""
        try:
            with open(STATS_FILE_PATH, "w", encoding="utf-8") as file:
                json.dump(statistics, file, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"Ошибка при сохранении статистики: {e}")

    @staticmethod
    def load_stats():
        """Загружает статистику из JSON-файла."""
        try:
            with open(STATS_FILE_PATH, "r", encoding="utf-8") as file:
                return json.load(file)
        except:
            return []  # Если файла нет, вернуть пустой список

    def add_session_statistics(self, statistics: list[dict], player_name: str, level_num: int):
        """Добавляет статистику текущей сессии."""
        game_session_stats = {
            "player_name": player_name,
            "treasure_collected": self.gold,
            "max_level": level_num,
            "enemies_defeated": self.enemies_defeated,
            "food_eaten": self.eaten_food,
            "elixirs_used": self.used_elixir,
            "scrolls_used": self.used_scrolls,
            "hits_dealt": self.hits_dealt,
            "hits_taken": self.hits_taken,
            "tiles_walked": self.tiles_walked,
        }
        statistics.append(game_session_stats)
        statistics.sort(key=lambda run: run.get(
            'treasure_collected', 0), reverse=True)
