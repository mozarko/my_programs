import curses

from constants.game_constants import *
from logic.game_session import GameSession


class Render:
    def __init__(self, stdscr: curses.window, win: curses.window):
        self.stdscr = stdscr
        self.init_colors()
        self.white = curses.color_pair(1)
        self.magenta = curses.color_pair(2)
        self.red = curses.color_pair(3)
        self.cyan = curses.color_pair(4)
        self.blue = curses.color_pair(5)
        self.green = curses.color_pair(6)
        self.yellow = curses.color_pair(7)
        self.win = win
        curses.curs_set(0)  # Отключить видимый курсор

    def init_colors(self):
        colors = [
            (1, curses.COLOR_WHITE, curses.COLOR_BLACK),
            (2, curses.COLOR_MAGENTA, curses.COLOR_BLACK),
            (3, curses.COLOR_RED, curses.COLOR_BLACK),
            (4, curses.COLOR_CYAN, curses.COLOR_BLACK),
            (5, curses.COLOR_BLUE, curses.COLOR_BLACK),
            (6, curses.COLOR_GREEN, curses.COLOR_BLACK),
            (7, curses.COLOR_YELLOW, curses.COLOR_BLACK),
            (8, curses.COLOR_BLACK, curses.COLOR_WHITE),
        ]

        for pair_id, fg_color, bg_color in colors:
            curses.init_pair(pair_id, fg_color, bg_color)

    def print_status_bar(self, session: GameSession):
        self.stdscr.addstr(0, 0, session.message_bar,
                           curses.A_BOLD | self.yellow)

        self.stdscr.addstr(MAP_HEIGHT + 3, 0,
                           f"Level: {session.level_num} | " +
                           f"HP: {session.player.cur_hp}/{session.player.max_hp + session.player.bonus_max_hp}(+{session.player.bonus_max_hp}) | " +
                           f"Str: {session.player.strength}(+{session.player.bonus_strength}) | " +
                           f"Agi: {session.player.agility}(+{session.player.bonus_agility}) | " +
                           f"Gold: {session.player.stats.gold}",
                           curses.A_BOLD | self.yellow)

        self.print_avaible_keys(session)
        self.print_info_bar()
        self.stdscr.refresh()

    def print_avaible_keys(self, game_session: GameSession):
        for i in range(len(COLOR_KEY_DOOR)):
            if COLOR_KEY_DOOR[i] not in game_session.level.keys.keys():
                self.stdscr.addstr(MAP_HEIGHT + 4, i * 2 + 6,
                                   f"& ", curses.color_pair(COLOR_KEY_DOOR[i]))
        self.stdscr.addstr(MAP_HEIGHT + 4, 0, f"Keys: ",
                           curses.A_BOLD | self.yellow)

    def print_info_bar(self):
        self.stdscr.addstr(
            MAP_HEIGHT + 5, 0, f'Backpack: (TAB) | Sword: (h) | Food: (j) | Elixir: (k) | Scroll: (e)', curses.A_BOLD | self.yellow)

    def print_field(self, session: GameSession):
        for x in range(MAP_WIDTH):
            for y in range(MAP_HEIGHT):
                wall = session.level.tiles[x][y].blocked
                if not wall:
                    self.check_sight(y, x, '.', session, self.green)
                else:
                    self.check_sight(y, x, '░', session, curses.color_pair(5))

        self.print_coridors_and_keys(session)

        for item in session.items:
            self.check_sight(item.y, item.x, item.symbol, session, self.white)

        self.check_sight(session.level.exit_door_y,
                         session.level.exit_door_x, EXIT_DOOR, session, self.magenta)

        for enemy in session.enemies:
            self.check_sight(enemy.y, enemy.x, enemy.symbol,
                             session, curses.color_pair(enemy.color))

        self.check_sight(int(round(session.player.y)), int(
            round(session.player.x)), session.player.symb, session, self.white)
        self.win.border()
        self.win.refresh()

    def refresh(self, game_session: GameSession):
        self.stdscr.clear()
        if game_session.is_3d:
            self.render_3d(game_session)
        self.print_status_bar(game_session)
        self.stdscr.refresh()
        self.print_field(game_session)

    def render_3d(self, session: GameSession):

        h, num_rays = self.stdscr.getmaxyx()
        delta_angle = FOV / num_rays
        proj_coeff = num_rays / (2 * math.tan(HALF_FOV))
        cur_angle = session.player.movement_strategy.player_angle - HALF_FOV
        x0, y0 = session.player.x, session.player.y

        for ray in range(num_rays):
            sin_a = math.sin(cur_angle)
            cos_a = math.cos(cur_angle)
            depth = 0
            bottom = h - 2  # Инициализируем bottom для случаев, когда стена не найдена

            while True:
                # Вычисляем координаты луча
                x = x0 + depth * cos_a
                y = y0 + depth * sin_a

                map_x, map_y = int(round(x)), int(round(y))

                if session.level.tiles[map_x][map_y].blocked:
                    # Корректируем глубину для устранения fisheye
                    depth *= math.cos(session.player.movement_strategy.player_angle - cur_angle)

                    # Рассчитываем высоту проекции
                    proj_height = min(proj_coeff / (depth + 0.0001), h - 2)

                    # Рассчитываем координаты для отрисовки
                    column = ray
                    color = self.blue if column % 2 == 0 else self.cyan
                    top = int((h - 2 - proj_height) / 2)
                    bottom = int((h - 2 + proj_height) / 2)

                    # Рисуем стену
                    for row in range(top, bottom):
                        self.stdscr.addch(row, column, '░', color)

                    break

                # Увеличиваем глубину для следующего шага луча
                depth += 0.1

            # Рисуем пол
            for row in range(bottom, h - 2):
                self.stdscr.addch(row, ray, '░')

            # Переходим к следующему углу
            cur_angle += delta_angle

    def print_coridors_and_keys(self, session: GameSession):
        """
        Выводит коридоры и ключи на экран.
        Args:
            session (GameSession): Сессия игры.
        """
        for corr in session.level.corridors:
            for x, y in corr.coordinates:
                self.check_sight(y, x, '▓', session,
                                 curses.color_pair(corr.color_idx))
                # Если коридор уже посещали, но он не находится в зоне видимости в данный момент, то выводит с другим цветом
                if (x, y) in session.level.visited_corridors and session.level.tiles[x][y].block_sight:
                    self.win.addch(y, x, '▒', curses.color_pair(4))

        for key in session.level.keys.values():
            self.check_sight(key.coordinates[1], key.coordinates[0],
                             key.symb, session, curses.color_pair(key.color_idx))

    def check_sight(self, y: int, x: int, symb: str, session: GameSession, color=None):
        """
        Проверяет, видима ли ячейка с координатами (x, y) и выводит символ на экран.
        Args:
            y (int): Координата y точки.
            x (int): Координата x точки.
            symb (str): Символ, который нужно вывести в точку.
            session (GameSession): Сессия игры.
            color (int, optional): Цвет символа. Если не указан, то символ выводится без цвета.
        """
        if not session.level.tiles[x][y].block_sight:
            if color:
                self.win.addch(y, x, symb, color)
            else:
                self.win.addch(y, x, symb)
        else:
            self.win.addch(y, x, ' ')
