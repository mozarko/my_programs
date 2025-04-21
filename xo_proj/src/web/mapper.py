from domain.model import GameSession


class WebMapper:
    @staticmethod
    def to_web_game_session_dict(domain_session: GameSession):
        """Преобразует GameSession в WebGameSession."""
        web_session_dict = {
            "game_id": domain_session.game_id,
            "board": domain_session.board.get_board(),
            "player_symbol": domain_session.get_player_symbol(),
            "player2_symbol": domain_session.player2_symbol,
            "computer_symbol": domain_session.get_computer_symbol(),
            "computer_first_move": domain_session.computer_first_move,
            "is_game_over": domain_session.is_game_over,
            "winner": domain_session.get_winner(),
            "user_id": domain_session.user_id,
            "user_login": domain_session.user_login,
            "user2_id": domain_session.user2_id,
            "user2_login": domain_session.user2_login,
            "multiplayer": domain_session.multiplayer,
            "statement": domain_session.current_state.get_current_state()
        }
        return web_session_dict
