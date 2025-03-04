import curses

from constants.game_constants import *
from datalayer.loading import Loading
from datalayer.stats import Stats
from logic.game_session import GameSession
from ui.ascii_images import *


def print_menu(stdscr: curses.window, selected_button_idx: int, bat_frame_idx: int, buttons: list):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    # creators
    creators_start_y = h - len(creators) - 5
    creators_start_x = w - len(creators[0]) - 5
    for idx, line in enumerate(creators):
        stdscr.addstr(creators_start_y + idx, creators_start_x, line)

    # rogue
    if w > 139 and h > 40:
        rogue_start_y = 1
        rogue_start_x = w // 2 - len(rogue_art[0]) // 2
        for idx, line in enumerate(rogue_art):
            stdscr.addstr(rogue_start_y + idx, rogue_start_x, line)

    # skull
    if h > 31:
        skull_start_y = h - len(skull) - 2
        skull_start_x = 1
        for idx, line in enumerate(skull):
            stdscr.addstr(skull_start_y + idx, skull_start_x, line)

    # bat
    bat_start_y = creators_start_y + 4
    bat_start_x = w // 2 - len(bat_frames[0][0]) // 2
    for idx, line in enumerate(bat_frames[bat_frame_idx]):
        stdscr.addstr(bat_start_y + idx, bat_start_x, line)

    # menu
    for idx, button in enumerate(buttons):
        x = w // 2 - len(button) // 2
        y = h // 2 - len(buttons) // 2 + idx
        if idx == selected_button_idx:
            stdscr.attron(curses.A_REVERSE)
            stdscr.addstr(y, x, button)
            stdscr.attroff(curses.A_REVERSE)
        else:
            stdscr.addstr(y, x, button)
    stdscr.refresh()


def print_art_on_center(stdscr: curses.window, art: list[str]):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    if h > 54 and w > 101:
        art_start_y = h // 2 - len(art) // 2
        art_start_x = w // 2 - len(art[0]) // 2
        for idx, line in enumerate(art):
            stdscr.addstr(art_start_y + idx, art_start_x, line)
    stdscr.refresh()


def handle_menu(stdscr: curses.window) -> GameSession | None:
    """Обработка выбора из главного меню."""
    while True:
        menu_choice = init_main_menu(stdscr, True)
        if menu_choice == 'New game':
            game_session = GameSession(player_name=get_player_name(stdscr))
            game_session.create_new_level()
            return game_session
        elif menu_choice == 'Load game':
            try:
                game_session = Loading.load_game()
                return game_session
            except:
                print_confirm_msg(stdscr, "Game loading error")
                stdscr.getch()
        elif menu_choice == 'Exit':
            return None
        elif menu_choice == 'Scoreboard':
            data = Stats().load_stats()
            print_scoreboard(stdscr, data)
            stdscr.getch()
        elif menu_choice == 'Help':
            print_help(stdscr)
            stdscr.getch()


def confirm_exit(stdscr: curses.window) -> str:
    print_confirm_msg(stdscr, "Are you sure you want to exit? (y/n)")
    key = stdscr.getch()
    if key in KEY_CONFIRM:
        return 'Exit'


def __confirm_load(stdscr: curses.window):
    print_confirm_msg(
        stdscr, "Do you want to load last saved game session? (y/n)")
    key = stdscr.getch()
    if key in KEY_CONFIRM:
        stdscr.clear()
        return 'Load game'


def init_main_menu(stdscr: curses.window, is_first: bool = False) -> str:
    stdscr.refresh()
    curses.curs_set(0)
    stdscr.keypad(True)
    current_button_idx = 0
    bat_frame_idx = 0

    while True:
        buttons = first_menu_buttons if is_first else main_menu_buttons
        print_menu(stdscr, current_button_idx, bat_frame_idx, buttons)

        key = stdscr.getch()

        if key in KEY_UP and current_button_idx > 0:
            current_button_idx -= 1
        elif key in KEY_DOWN and current_button_idx < len(buttons) - 1:
            current_button_idx += 1
        elif key in KEY_ENTER:
            selected_button = buttons[current_button_idx]
            if selected_button == 'Exit':
                return confirm_exit(stdscr)
            elif selected_button == 'Scoreboard':
                stdscr.clear()
                return 'Scoreboard'
            elif selected_button == 'New game':
                stdscr.clear()
                return 'New game'
            elif selected_button == 'Continue':
                stdscr.clear()
                return 'Continue'
            elif selected_button == 'Load game':
                stdscr.clear()
                return __confirm_load(stdscr)
            elif selected_button == 'Save game':
                stdscr.clear()
                return 'Save game'
            elif selected_button == 'Help':
                stdscr.clear()
                return 'Help'

        bat_frame_idx = (bat_frame_idx + 1) % len(bat_frames)


def get_player_name(stdscr: curses.window) -> str:
    h, w = stdscr.getmaxyx()
    stdscr.clear()
    stdscr.addstr(h // 2 - 1, w // 2 - len("Enter your name") //
                  2, "Enter your name")
    stdscr.refresh()

    name = ""
    while True:
        key = stdscr.getch()

        if key in KEY_ENTER:  # Enter
            stdscr.clear()
            break
        elif key in (8, 127):  # Backspace
            if len(name) > 0:
                name = name[:-1]

        elif 32 <= key <= 126:  # Printable characters
            name += chr(key)

        # Clear the name line and redraw centered
        stdscr.addstr(h // 2, 0, " " * w)  # Clear the line
        start_x = w // 2 - len(name) // 2
        stdscr.addstr(h // 2, start_x, name, curses.A_BOLD)
        stdscr.refresh()

    return name


def print_confirm_msg(stdscr: curses.window, msg: str):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    stdscr.addstr(h // 2, (w // 2) - (len(msg) // 2), msg, curses.A_BOLD)
    stdscr.refresh()


def print_scoreboard(stdscr: curses.window, data, start_y=0, start_x=0):
    stdscr.clear()
    _, w = stdscr.getmaxyx()

    # Заголовки таблицы
    headers = ["Name", "Treasures", "Level", "Enemies", "Food", "Elixirs",
               "Scrolls", "Hits dealt", "Hits Taken", "Moves"]
    stdscr.addstr(start_y, start_x, " | ".join(
        f"{header:^10}" for header in headers))
    stdscr.addstr(start_y + 1, start_x, "-" * w)

    # Данные
    for row_idx, row in enumerate(data, start=start_y + 2):
        row_values = [
            row["player_name"],
            row["treasure_collected"],
            row["max_level"],
            row["enemies_defeated"],
            row["food_eaten"],
            row["elixirs_used"],
            row["scrolls_used"],
            row["hits_dealt"],
            row["hits_taken"],
            row["tiles_walked"],
        ]
        stdscr.addstr(row_idx, start_x, " | ".join(
            f"{str(value):^10}" for value in row_values))

    stdscr.refresh()


def print_help(stdscr: curses.window):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    help_info = [
        "       Main menu:              ESC      ",
        "       Backpack/buffs:         TAB      ",
        "       3D mode on/off:         z        ",
        "       Equip a sword:          h        ",
        "       Eat food:               j        ",
        "       Read a scroll:          e        ",
        "       Drink elixir:           k        ",
        "       Attack an enemy:        SPACE    ",
        "       Movements:              w,a,s,d  "
    ]
    for idx, row in enumerate(help_info):
        x = w // 2 - len(row) // 2
        y = h // 2 - len(help_info) // 2 + idx
        stdscr.addstr(y, x, row, curses.A_BOLD)

    stdscr.refresh()
