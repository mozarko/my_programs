from constants.game_constants import *


class AutoLeveling:
    def __init__(self, enemies_num: int, items_num: int, enemies: list, player):
        self.enemies_num = enemies_num
        self.items_num = items_num
        self.enemies = enemies
        self.player = player
        self.enemies_defeated = 0
        self.hits_dealt = 0
        self.hits_taken = 0
        self.eaten_food = 0
        self.used_elixir = 0
        self.enemy_health_coeff_value = None

    def reset_counters(self):
        """Сбрасывает статистику после уровня"""
        self.enemies_defeated = 0
        self.hits_dealt = 0
        self.hits_taken = 0
        self.eaten_food = 0
        self.used_elixir = 0

    def end_calculate_difficulty_coefficients(self):
        """Рассчитывает коэффициенты сложности при окончании уровня."""

        LVL_GEN_COEF["enemies_count"] = (
            1.5 if self.kills_coeff() <= 1.4 else
            0.7 if self.kills_coeff() > 3 else
            1.0
        )

        LVL_GEN_COEF["items_healing"] = (
            3 if self.healing_coeff() < 0.2 else
            2 if self.healing_coeff() < 0.5 else
            1 if self.healing_coeff() < 0.8 else
            0 if self.healing_coeff() < 1 else
            -2 if self.healing_coeff() > 1 else
            -1
        )
        
        LVL_GEN_COEF["items_count"] = self.apply_limits(
            self.items_using_coeff())

    def start_calculate_difficulty_coefficients(self):
        """Рассчитывает коэффициенты сложности в начале уровня."""
        self.enemy_health_coeff_value = self.enemies_health_coeff()

        LVL_GEN_COEF["enemies_health_stats"] = (
            1.5 if self.enemy_health_coeff_value <= 2 else
            1.2 if self.enemy_health_coeff_value < 3 else
            0.8 if self.enemy_health_coeff_value > 5 else
            0.5 if self.enemy_health_coeff_value > 6 else
            1.0
        )

    def dmg_ratio_coeff(self) -> float:
        """Соотношение между полученным и нанесённым уроном"""
        return (self.hits_dealt + 1) / self.hits_taken if self.hits_taken else 1

    def kills_coeff(self) -> float:
        """Соотношение между убитыми врагами к общему числу врагов на уровне"""
        return (self.enemies_num + 1) / (self.enemies_defeated + 1)

    def items_using_coeff(self) -> float:
        """Соотношение между использованием аптечек и эликсиров к общему числу предметов на уровне"""
        if self.used_elixir + self.eaten_food != 0:
            return (self.items_num + 1) / ((self.used_elixir + self.eaten_food) * 2)
        return 1.0

    def healing_coeff(self) -> float:
        """Соотношение текущего здоровья к максимальному здоровью героя"""
        return self.player.cur_hp / self.player.max_hp

    def avg_dmg_to_kill(self):
        """Соотношение нанесенных ударов по врагам к количеству побежденных врагов"""
        # из расчёта 3 удара на врага
        return self.hits_dealt * 3 / (self.enemies_defeated + 1) if self.hits_dealt else 1

    def enemies_health_coeff(self) -> float:
        """Соотношение среднего здоровья врагов к силе героя
        (по сути показывает кол-во ударов для убийства врага без учета ловкости"""
        enemies_health_sum = 0
        for enemy in self.enemies:
            enemies_health_sum += enemy.max_hp
        return (enemies_health_sum / len(self.enemies)) / self.player.strength / 1.3

    def apply_limits(self, value: float, min_value: float = 0.5, max_value: float = 1.5) -> float:
        # Ограничение коэффициентов
        return max(min_value, min(max_value, value))
