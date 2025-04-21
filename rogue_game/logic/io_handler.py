import curses

from logic.game_session import GameSession
from datalayer.stats import Stats
from constants.game_constants import *
from ui.main_menu_window import *
import ui.render as Render
from datalayer.loading import Loading
from datalayer.saving import Saving


class IOHandler:
    def __init__(self, game_session: GameSession, render: Render, stdscr: "curses.window", win):
        self.game_session = game_session
        self.stdscr = stdscr
        self.win = win
        self.render = render

    def __confirm_using_dialog(self) -> int | None:
        idx = self.win.getch()
        if idx is not None and 49 <= idx <= 57:
            return idx - 48

        return None

    def msg_bar_item_handler(self, item_type: str, action: str):
        items = self.game_session.player.get_items_by_type(item_type)
        if not items:
            self.game_session.message_bar = f"You don't have any {item_type}s in your backpack!"
        else:
            items_with_idx = [f"{item}[{idx + 1}]" for idx,
                              item in enumerate(items)]
            self.game_session.message_bar = f"Available {item_type}s: " + \
                ", ".join(map(str, items_with_idx))
            self.game_session.message_bar += f".\nChoose {item_type} to {action}...(1-9)"
        return items

    def io_item_handler(self, items, item_type: str, action_method):
        idx = self.__confirm_using_dialog()
        if idx is not None and 1 <= idx <= len(items):
            if item_type == 'sword':
                self.game_session.message_bar, prev_sword = action_method(
                    items, idx - 1)
                if prev_sword is not None:
                    self.game_session.items.append(prev_sword)
            else:
                self.game_session.message_bar = action_method(items, idx - 1)
                if item_type == 'elixir':
                    self.game_session.autolvl.used_elixir += 1
                elif item_type == 'food':
                    self.game_session.autolvl.eaten_food += 1
        else:
            self.game_session.message_bar = f"Invalid {item_type} selection!"

    def input_checking(self, key, char) -> int:
        if key == KEY_ESC:
            while True:
                menu_choice = init_main_menu(self.stdscr)
                if menu_choice == 'Exit':
                    return 0
                elif menu_choice == 'Save game':
                    try:
                        Saving.save_game(self.game_session)
                        print_confirm_msg(
                            self.stdscr, "Game was successfully saved")
                        self.stdscr.getch()
                    except:
                        print_confirm_msg(self.stdscr, "Game saving error")
                        self.stdscr.getch()
                    self.stdscr.refresh()
                elif menu_choice == 'Load game':
                    try:
                        self.game_session = Loading.load_game()
                        return 5
                    except:
                        print_confirm_msg(self.stdscr, "Game loading error")
                        self.stdscr.getch()
                        self.stdscr.refresh()
                elif menu_choice == 'New game':
                    return 6
                elif menu_choice == 'Scoreboard':
                    data = Stats().load_stats()
                    print_scoreboard(self.stdscr, data)
                    self.stdscr.getch()
                elif menu_choice == 'Help':
                    print_help(self.stdscr)
                    self.stdscr.getch()
                elif menu_choice == 'Continue':
                    break

        elif key == KEY_OPEN_BACKPACK:
            return 1
        elif char in {'h', 'k', 'j', 'e'}:
            return 2
        elif char in DIRECTION_MAP:
            return 3
        elif key in KEY_MODE_3D:
            return 4
        else:
            return None
