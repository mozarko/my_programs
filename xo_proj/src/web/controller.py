# controller.py
from flask import request, jsonify, session
from uuid import uuid4
from di.container import Container
from web.mapper import WebMapper
from domain.model import GameSession


class Controller:

    @staticmethod
    def check_active_games():
        repository = Container.get('repository')
        game_session = repository.get_last_active_game(session["user_id"])
        return game_session


    @staticmethod
    def new_multi_game():
        """Создает новую игровую сессию и возвращает web_session_dict."""
        data = request.json
        player_symbol = data["player_symbol"]
        player2_symbol = "O" if player_symbol == "X" else "X"
        new_game_id = str(uuid4())
        game_session = (GameSession
                        (game_id=new_game_id,
                         player_symbol=player_symbol,
                         player2_symbol=player2_symbol,
                         user_id=session["user_id"],
                         user_login=session["user_login"],
                         multiplayer=True))
        repository = Container.get('repository')
        repository.save_game(game_session)

        return jsonify(WebMapper.to_web_game_session_dict(game_session)), 200

    @staticmethod
    def join_game(game_id: str):
        """Подключает текущего пользователя как второго игрока"""
        repository = Container.get('repository')
        game_session = repository.get_game(game_id)
        # Обновляем данные игры
        if not game_session.user2_id and game_session.user2_id != session["user_id"]:
            game_session.user2_id = session["user_id"]
            game_session.user2_login = session["user_login"]
            if game_session.current_state.get_current_state() == "waiting_players":
                if game_session.player_symbol == "X":
                    game_session.current_state.set_move(game_session.user_login)
                if game_session.player2_symbol == "X":
                    game_session.current_state.set_move(game_session.user2_login)
        repository.save_game(game_session)

    @staticmethod
    def update_game_multi(game_id: str):
        """Обрабатывает ход игрока и делает ход компьютера"""
        # Получаем игровую сессию
        repository = Container.get('repository')
        game_session = repository.get_game(game_id)
        service = Container.get('service')

        data = request.json
        repository = Container.get('repository')
        row, col = data["row"], data["col"]

        # Проверяем, свободна ли ячейка
        if game_session.get_board().get_cell(row, col) != 0:
            return jsonify({"error": "Cell is already occupied"}), 400

        player_symbol_value = None

        if session["user_id"] == game_session.user_id:
            player_symbol_value = 1 if game_session.player_symbol == "X" else 2

        if session["user_id"] == game_session.user2_id:
            player_symbol_value = 1 if game_session.player2_symbol == "X" else 2

        # Ход игрока
        game_session.get_board().set_cell(row, col, player_symbol_value)
        # Проверяем закончился ли ход первого игрока
        Controller.check_is_game_over_session_multi(service, game_session)
        if game_session.is_game_over:
            repository.save_game(game_session)
            return jsonify(WebMapper.to_web_game_session_dict(game_session)), 200
        # Ставим ход следующего игрока
        next_player = game_session.user2_login if game_session.user_login == session[
            "user_login"] else game_session.user_login
        game_session.current_state.set_move(str(next_player))
        Controller.check_is_game_over_session_multi(service, game_session)
        repository.save_game(game_session)
        return jsonify(WebMapper.to_web_game_session_dict(game_session)), 200

    @staticmethod
    def new_game():
        """Создает новую игровую сессию и возвращает web_session_dict."""
        data = request.json
        player_symbol = data["player_symbol"]
        computer_symbol = "O" if player_symbol == "X" else "X"
        computer_first_move = True if player_symbol == "O" else False

        new_game_id = str(uuid4())
        game_session = GameSession(game_id=new_game_id, player_symbol=player_symbol, computer_symbol=computer_symbol,
                                   computer_first_move=computer_first_move, user_id=session["user_id"],
                                   user_login=session["user_login"])
        repository = Container.get('repository')
        repository.save_game(game_session)

        return jsonify(WebMapper.to_web_game_session_dict(game_session)), 200

    @staticmethod
    def get_game(game_id: str):
        """Возвращает текущее состояние игры."""
        repository = Container.get('repository')
        game_session = repository.get_game(game_id)
        if not game_session:
            return jsonify({"error": f"Game with ID {game_id} not found"}), 404
        return jsonify(WebMapper.to_web_game_session_dict(game_session)), 200

    @staticmethod
    def update_game(game_id: str):
        """Обрабатывает ход игрока и делает ход компьютера"""
        # Получаем игровую сессию
        repository = Container.get('repository')
        game_session = repository.get_game(game_id)
        service = Container.get('service')

        data = request.json
        if data == "computer_first_move":
            row, col = service.get_next_move(game_session)
            game_session.get_board().set_cell(row, col, 1)
            game_session.computer_first_move = False
            game_session.current_state.set_move(str(session["user_login"]))
            repository.save_game(game_session)
            return '', 204

        repository = Container.get('repository')
        row, col = data["row"], data["col"]

        # Проверяем, свободна ли ячейка
        if game_session.get_board().get_cell(row, col) != 0:
            return jsonify({"error": "Cell is already occupied"}), 400

        player_symbol_value = 1 if game_session.get_player_symbol() == "X" else 2
        computer_symbol_value = 2 if player_symbol_value == 1 else 1

        # Ход игрока
        game_session.get_board().set_cell(row, col, player_symbol_value)
        game_session.current_state.set_move(str(session["user_login"]))
        # Проверяем, закончилась ли игра после хода игрока
        is_game_over = Controller.check_is_game_over_session(service, game_session)
        if is_game_over is None:
            row, col = service.get_next_move(game_session)
            game_session.get_board().set_cell(row, col, computer_symbol_value)
        # Проверяем, закончилась ли игра после хода компьютера
        Controller.check_is_game_over_session(service, game_session)
        repository.save_game(game_session)
        return jsonify(WebMapper.to_web_game_session_dict(game_session)), 200

    @staticmethod
    def check_is_game_over_session(service, game_session):
        # Проверяем, закончилась ли игра после хода
        if service.is_game_over(game_session):
            game_session.set_winner(service.get_winner(game_session))
            if game_session.get_winner() == "draw":
                game_session.current_state.set_draw()
            elif game_session.get_winner() == "player":
                game_session.current_state.set_winner(session["user_login"])
            elif game_session.get_winner() == "computer":
                game_session.current_state.set_computer_winner()
            game_session.is_game_over = True
            return True
        else:
            return None

    @staticmethod
    def check_is_game_over_session_multi(service, game_session):
        # Проверяем, закончилась ли игра после хода
        winner = service.check_winner(board=game_session.get_board().get_board(), mode="multi")
        if winner:
            game_session.is_game_over = True
        if winner == "draw":
            game_session.current_state.set_draw()
            game_session.set_winner("draw")
        if winner == "playerX":
            if game_session.player_symbol == "X":
                game_session.current_state.set_winner(game_session.user_login)
                game_session.set_winner(game_session.user_login)
            else:
                game_session.current_state.set_winner(game_session.user2_login)
                game_session.set_winner(game_session.user2_login)
        if winner == "playerO":
            if game_session.player_symbol == "O":
                game_session.current_state.set_winner(game_session.user_login)
                game_session.set_winner(game_session.user_login)
            else:
                game_session.current_state.set_winner(game_session.user2_login)
                game_session.set_winner(game_session.user2_login)

    @staticmethod
    def get_all_games():
        repository = Container.get('repository')
        all_games = repository.get_all_games_single(session["user_id"])
        all_games_single = []
        for game in all_games:
            if not game.multiplayer:
                all_games_single.append(game)
        return all_games_single

    @staticmethod
    def get_all_games_multi():
        repository = Container.get('repository')
        all_games = repository.get_all_games_multi()
        all_games_multi = []
        for game in all_games:
            if game.multiplayer:
                all_games_multi.append(game)
        return all_games_multi
