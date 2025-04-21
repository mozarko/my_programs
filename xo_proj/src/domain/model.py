# model.py
from enum import Enum
from dataclasses import dataclass


class User:
    def __init__(self, user_id: int, uid: str, login: str, password: str):
        self.user_id = user_id
        self.uid = uid
        self.login = login
        self.password = password

    def __repr__(self):
        return f"User(id={self.user_id}, uid={self.uid}, login={self.login}, password={self.password})"


class GameBoard:
    def __init__(self, board=None):
        self.size = 3
        self.board = board if board is not None else [[0 for _ in range(self.size)] for _ in range(self.size)]

    def get_board(self) -> list[list[int]]:
        return self.board

    def set_cell(self, row: int, col: int, value: int) -> None:
        if 0 <= row < self.size and 0 <= col < self.size:
            self.board[row][col] = value
        else:
            raise ValueError("Invalid cell coordinates")

    def get_cell(self, row: int, col: int) -> int:
        return self.board[row][col]

    def __str__(self) -> str:
        return "\n".join(" ".join(map(str, row)) for row in self.board)


class GameState(Enum):
    WAITING_PLAYERS = "waiting_players"
    MOVE_PLAYER = "move_player"
    DRAW = "draw"
    WIN_PLAYER = "win_player"
    WIN_COMPUTER = "win_computer"


@dataclass
class State:
    status: GameState
    user_login: str | None = None


class Statements:
    def __init__(self):
        self.current_state = State(GameState.WAITING_PLAYERS)

    def set_move(self, user_login: str):
        self.current_state = State(GameState.MOVE_PLAYER, user_login)

    def set_winner(self, user_login: str):
        self.current_state = State(GameState.WIN_PLAYER, user_login)

    def set_computer_winner(self):
        self.current_state = State(GameState.WIN_COMPUTER)

    def set_draw(self):
        self.current_state = State(GameState.DRAW)

    def get_current_state(self):
        return f"{self.current_state.status.value} {self.current_state.user_login}" if self.current_state.user_login else self.current_state.status.value


class GameSession:

    def __init__(self, game_id: str,
                 player_symbol: str,
                 user_id: int,
                 user_login: str,
                 player2_symbol: str = None,
                 computer_symbol: str = None,
                 computer_first_move: bool = None,
                 user2_id: int = None,
                 user2_login: str = None,
                 multiplayer: bool = False,
                 board: GameBoard = None,
                 is_game_over: bool = False,
                 winner: str = None,
                 current_state: Statements = Statements()):
        self.game_id = game_id
        self.board = board if board is not None else GameBoard()
        self.player_symbol = player_symbol
        self.player2_symbol = player2_symbol
        self.computer_symbol = computer_symbol
        self.computer_first_move = computer_first_move
        self.is_game_over = is_game_over
        self._winner = winner
        self.user_id = user_id
        self.user_login = user_login
        self.user2_id = user2_id
        self.user2_login = user2_login
        self.multiplayer = multiplayer
        self.current_state = current_state

    def get_game_id(self) -> str:
        return self.game_id

    def get_board(self) -> GameBoard:
        return self.board

    def get_player_symbol(self):
        return self.player_symbol

    def get_computer_symbol(self):
        return self.computer_symbol

    def get_winner(self):
        return self._winner

    def set_winner(self, winner):
        self._winner = winner

    def __str__(self) -> str:
        return (f"Game ID: {self.game_id}\n"
                f"Board:\n{self.board}\n"
                f"Player Symbol: {self.player_symbol}\n"
                f"Player2 Symbol: {self.player2_symbol}\n"
                f"Computer Symbol: {self.computer_symbol}\n"
                f"Computer First Move: {self.computer_first_move}\n"
                f"User ID: {self.user_id}\nUser Login: {self.user_login}\n"
                f"User2 ID: {self.user2_id}\nUser2 Login: {self.user2_login}\n"
                f"Multiplayer: {self.multiplayer}\nIs Game Over: {self.is_game_over}\n"
                f"Winner: {self._winner}\n"
                f"State: {self.current_state.get_current_state()}\n")

    def __repr__(self):
        return self.__str__()
