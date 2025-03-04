from __future__ import annotations
import curses

from constants.game_constants import *
from datalayer.saving import Saving
from logic.game_session import GameSession
from logic.io_handler import IOHandler
from ui.render import Render
from ui.main_menu_window import *
import utils


def main(stdscr: "curses.window"):
    win = curses.newwin(MAP_HEIGHT + 1,
                        MAP_WIDTH + 1, 2, 0)

    game_session = handle_menu(stdscr)
    if not game_session:
        return

    render = Render(stdscr, win)
    io_handler = IOHandler(game_session, render, stdscr, win)
    render.print_status_bar(game_session)
    render.print_field(game_session)

    while True:
        if game_session.player.is_dead():
            print_art_on_center(stdscr, game_over_screen)
            stdscr.getch()
            break

        if game_session.check_item_pickup():
            render.refresh(game_session)

        key = win.getch()
        char = chr(key).lower() if key != -1 else None
        input_res = io_handler.input_checking(key, char)

        if input_res == 0:      # exit
            break
        elif input_res == 1:    # show backpack
            utils.open_backpack(game_session, render)
        elif input_res == 2:    # item
            utils.items_action(game_session, render, char, io_handler)
        elif input_res == 3:    # move
            utils.move(char, game_session, render)
        elif input_res == 4:
            utils.toggle_view(game_session, render)
        elif input_res == 5:    # load_game
            render.refresh(game_session)
            continue
        elif input_res == 6:    # new game
            game_session = GameSession(get_player_name(stdscr))
            game_session.create_new_level()
            render.refresh(game_session)
            continue
        else:                   # menu
            render.refresh(game_session)

        # Перемещение врагов
        game_session.enemies_step()

        # Проверка на начало боя
        if game_session.check_for_combat():
            utils.handle_combat(game_session, render, win)

        if game_session.is_exit_door():
            try:
                Saving.save_game(game_session)
            except:
                print_confirm_msg(stdscr, "Game saving error")
                stdscr.getch()
            if game_session.level_num == MAX_LEVELS:
                print_art_on_center(stdscr, win_art)
                stdscr.getch()
                break
            game_session.create_new_level()
            render.refresh(game_session)

    utils.sending_stats(game_session)


curses.wrapper(main)
