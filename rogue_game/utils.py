from datalayer.stats import Stats
from constants.game_constants import *
from logic.game_session import GameSession
from logic.movement_strategies import PlayerMovementStrategy3D, PlayerMovementStrategy
from ui.render import Render
from ui.main_menu_window import *


def toggle_view(game_session: GameSession, render: Render):
    """Переключение между 2D и 3D режимами."""
    if game_session.is_3d:
        game_session.is_3d = False
        game_session.player.movement_strategy = PlayerMovementStrategy()
        game_session.player.x = round(game_session.player.x)
        game_session.player.y = round(game_session.player.y)
    else:
        game_session.is_3d = True
        game_session.player.movement_strategy = PlayerMovementStrategy3D()
    render.refresh(game_session)


def handle_combat(game_session: GameSession, render: Render, win: curses.window):
    """Цикл боя."""
    while game_session.in_combat:
        render.refresh(game_session)
        key = win.getch()
        if key == KEY_SPACE:
            game_session.combat_turn()
            render.refresh(game_session)


def items_action(game_session: GameSession, render: Render, char, io_handler):
    """Использование предмета"""
    # Writing info about items into bar
    items = io_handler.msg_bar_item_handler(
        ITEM_USE[char][0], ITEM_USE[char][1])
    render.refresh(game_session)
    if not items:
        return

    # Doing action and writing about one
    action_name = f"{ITEM_USE[char][1]}_{ITEM_USE[char][0]}"
    action_method = getattr(game_session.player, action_name)
    io_handler.io_item_handler(items, ITEM_USE[char][0], action_method)
    if action_method == 'eat_food':
        game_session.autolvl.eaten_food += 1
    elif action_method == 'use_elixir':
        game_session.autolvl.used_elixir += 1
    render.refresh(game_session)


def open_backpack(game_session: GameSession, render: Render):
    game_session.message_bar = str(game_session.player.backpack) + '\n'
    game_session.message_bar += 'Active buffs: ' + \
        str(game_session.player.active_buffs)
    render.refresh(game_session)


def move(char, game_session: GameSession, render: Render):
    game_session.player.move(game_session.level, char)
    game_session.level.clear_fog_of_war(
        game_session.player.x, game_session.player.y)
    render.refresh(game_session)


def sending_stats(game_session: GameSession):
    statistic = Stats().load_stats()
    game_session.player.stats.add_session_statistics(
        statistic, game_session.player_name, game_session.level_num)
    Stats().save_stats(statistic)
