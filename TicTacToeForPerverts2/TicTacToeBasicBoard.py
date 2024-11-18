from typing import Tuple

# Класс TicTacToeBasicBoard реализует основные функциональные возможности, которые доступны как на местном,
# так и на глобальных доски участвуют в суперигре в крестики-нолики. Этот класс является
# предназначен для использования в качестве родительского класса для классов Tic Tac Toe Board и
# SuperTicTacToe oard.
class TicTacToeBasicBoard:

    def __init__(self, topleft: Tuple[float, float], width: int) -> None:
        self.board = None
        self.topleft = topleft
        self.width = width

    def winner(self):

        board = [e.winner() for e in self.board]
        for player in (1, 2):
            winner_comb = [player] * 3
            # проверять победителя по строкам
            for i in range(0, 9, 3):
                row = [board[i], board[i+1], board[i+2]]
                if row == winner_comb:
                    return player
            # проверять победителя по столбцам
            for j in range(3):
                col = [board[j], board[j+3], board[j+6]]
                if col == winner_comb:
                    return player
            # проверять победителя по диагоналям
            asc_diag = [board[0], board[4], board[8]]
            if asc_diag == winner_comb:
                return player
            desc_diag = [board[6], board[4], board[2]]
            if desc_diag == winner_comb:
                return player

        # если победителя нет, проверьте, закончилась ли игра вничью
        num_filled_cells = 0
        for cell_state in board:
            num_filled_cells += int(cell_state > 0)

        # если num_filled_cells равно 9, то в игре нет разрешенных ходов: ничья
        return -1 if num_filled_cells == 9 else 0

    # метод __getitem__ используется для доступа к элементам доски
    def __getitem__(self, idx):

        return self.board[idx]
