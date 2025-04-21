from random import randint

class MinimaxGameService:

    def get_winner(self, session):
        return self.check_winner(board=session.get_board().get_board(), player_symbol=session.player_symbol)

    def get_next_move(self, session) -> tuple[int, int]:
        """
        Возвращает оптимальный ход для компьютера с использованием алгоритма Минимакс.
        """
        board = session.get_board().get_board()
        player_symbol = session.get_player_symbol()
        best_score = -float("inf")
        move = (-1, -1)
        if session.computer_first_move:
            move = (randint(0, 2), randint(0, 2))

        if not session.computer_first_move:
            if player_symbol == "X":
                # Приоритетные клетки: центр, углы, края
                priority_cells = [(1, 1), (0, 0), (0, 2), (2, 0), (2, 2), (0, 1), (1, 0), (1, 2), (2, 1)]
                for (i, j) in priority_cells:
                    if board[i][j] == 0:  # Если клетка пуста
                        board[i][j] = 2  # Ход компьютера (нолик)
                        score = self._minimax(board, player_symbol, 0, False)
                        board[i][j] = 0  # Отменяем ход
                        if score > best_score:
                            best_score = score
                            move = (i, j)

            if player_symbol == "O":
                for i in range(3):
                    for j in range(3):
                        if board[i][j] == 0:  # Если клетка пуста
                            board[i][j] = 1  # Ход компьютера (крестик)
                            score = self._minimax(board, player_symbol, 0, True)
                            board[i][j] = 0  # Отменяем ход
                            if score > best_score:
                                best_score = score
                                move = (i, j)

        return move

    def _minimax(self, board: list[list[int]], player_symbol: str, depth: int, is_maximizing: bool) -> int:
        """
        Рекурсивный алгоритм Минимакс для оценки ходов.
        """
        result = self.check_winner(board=board, player_symbol=player_symbol)
        if result is not None:
            # Интерпретируем результат _check_winner
            if result == "computer":  # Компьютер выиграл
                return 10 - depth
            elif result == "player":  # Игрок выиграл
                return depth - 10
            else:  # Ничья
                return 0

        return self.calc_best_score(board, player_symbol, depth, is_maximizing)

    def calc_best_score(self, board, player_symbol, depth, is_maximizing):

        if is_maximizing:
            best_score = -float("inf")
            for i in range(3):
                for j in range(3):
                    if board[i][j] == 0:
                        board[i][j] = 2  # Ход компьютера (нолик)
                        score = self._minimax(board, player_symbol, depth + 1, False)
                        board[i][j] = 0  # Отменяем ход
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float("inf")
            for i in range(3):
                for j in range(3):
                    if board[i][j] == 0:
                        board[i][j] = 1  # Ход игрока (крестик)
                        score = self._minimax(board, player_symbol, depth + 1, True)
                        board[i][j] = 0  # Отменяем ход
                        best_score = min(score, best_score)
            return best_score

    def is_game_over(self, session) -> bool:
        """
        Проверяет, закончена ли игра.
        """
        board = session.get_board().get_board()
        player_symbol = session.player_symbol
        return self.check_winner(board=board, player_symbol=player_symbol) is not None

    @staticmethod
    def check_winner(board: list[list[int]], mode: str = "single", player_symbol: str = "X") -> str | None:
        """
        Проверяет, есть ли победитель или ничья на поле.
        mode: 'single' — одиночная игра, 'multi' — мультиплеер.
        """
        player_value = 1 if player_symbol == "X" else 2

        lines = (
                board +
                list(zip(*board)) +
                [(board[0][0], board[1][1], board[2][2]),
                 (board[0][2], board[1][1], board[2][0])]
        )

        for line in lines:
            if line[0] == line[1] == line[2] != 0:
                if mode == "single":
                    return "player" if line[0] == player_value else "computer"
                elif mode == "multi":
                    return "playerX" if line[0] == 1 else "playerO"

        return "draw" if all(cell != 0 for row in board for cell in row) else None
