# route.py
from flask import Blueprint, render_template, redirect
from web.controller import Controller
from web.user_auth_controller import UserAuthController

# Создаем Blueprint для маршрутов
routes = Blueprint('routes', __name__)


# Регистрируем маршруты
# Game routes
@routes.route("/")
def index():
    return render_template("index.html")

# Multi game
@routes.route("/multiplayer")
@UserAuthController.login_required
def multiplayer():
    return render_template("multiplayer.html")


@routes.route("/multiplayer_game/")
@UserAuthController.login_required
def multiplayer_game():
    return render_template("multiplayer_game.html")


@routes.route("/multiplayer_continue/")
@UserAuthController.login_required
def multiplayer_continue():
    active_game = Controller.check_active_games()
    if active_game:
        return render_template("multiplayer_joingame.html", game_id=active_game.game_id)
    else:
        return render_template("multiplayer_game.html")


@routes.route("/new_multi_game", methods=["POST"])
@UserAuthController.login_required
def new_multi_game_route():
    """Маршрут для создания новой игровой сессии."""
    return Controller.new_multi_game()


@routes.route("/join_game/<string:game_id>", methods=["GET"])
@UserAuthController.login_required
def join_game(game_id):
    """Маршрут для присоединения к существующей игре"""
    Controller.join_game(game_id)
    return render_template("multiplayer_joingame.html", game_id=game_id)


@routes.route("/game_multi/<string:game_id>", methods=["POST"])
@UserAuthController.login_required
def update_game_multi_route(game_id: str):
    """Маршрут для обработки хода игрока и хода компьютера."""
    return Controller.update_game_multi(game_id)


@routes.route('/multiplayer_games_list', methods=['GET'])
@UserAuthController.login_required
def show_games_list_multi():
    all_games_multi = Controller.get_all_games_multi()
    return render_template("games_list_multi.html", games=all_games_multi)

# Single game
@routes.route("/xo")
@UserAuthController.login_required
def game_xo():
    return render_template("xo.html")


@routes.route("/new_game", methods=["POST"])
@UserAuthController.login_required
def new_game_route():
    """Маршрут для создания новой игровой сессии."""
    return Controller.new_game()


@routes.route("/game/<string:game_id>", methods=["GET"])
@UserAuthController.login_required
def get_game_route(game_id: str):
    """Маршрут для получения текущего состояния игры."""
    return Controller.get_game(game_id)


@routes.route("/game/<string:game_id>", methods=["POST"])
@UserAuthController.login_required
def update_game_route(game_id: str):
    """Маршрут для обработки хода игрока и хода компьютера."""
    return Controller.update_game(game_id)


@routes.route('/games_list', methods=['GET'])
@UserAuthController.login_required
def show_games_list():
    all_games_single = Controller.get_all_games()
    return render_template("games_list.html", games=all_games_single)


@routes.route("/continue/<string:game_id>")
@UserAuthController.login_required
def continue_game(game_id: str):
    """Главная страница. Клиент должен получить game_id самостоятельно."""
    return render_template("continue.html", game_id=game_id)


# Auth routes
@routes.route('/register', methods=['GET'])
@UserAuthController.already_logged_in
def show_register_form():
    """Маршрут для отображения страницы регистрации."""
    return render_template("user_register.html")


@routes.route('/register', methods=['POST'])
def user_register_route():
    """Маршрут для обработки регистрации пользователя."""
    return UserAuthController.user_register()


@routes.route('/login', methods=['GET'])
@UserAuthController.already_logged_in
def show_login_form():
    """Маршрут для отображения страницы входа."""
    return render_template("user_login.html")


@routes.route('/login', methods=['POST'])
def user_login_route():
    """Маршрут для обработки входа пользователя."""
    return UserAuthController.user_login()


@routes.route('/logout', methods=['GET'])
def user_logout():
    """Маршрут для выхода пользователя."""
    return UserAuthController.logout()


@routes.route('/user_info', methods=['GET'])
@UserAuthController.login_required
def user_info():
    return render_template("user_info.html")
