import pygame
from typing import Optional, Tuple
from TicTacToeCell import TicTacToeCell
from TicTacToeBasicBoard import TicTacToeBasicBoard

#  Класс TicTacToeBoard реализует функциональные возможности доски для игры в крестики-нолики.
#  Наследует функциональные возможности от базового класса доски для игры в крестики-нолики.
#  Заполняет атрибут доски 9 ячейками для игры в крестики-нолики (сетка 3х3).
class TicTacToeBoard(TicTacToeBasicBoard):

    # Процент от ширины, которая использовалась для создания разделения между ячейками
    cell_dist_pct = 0.10

    def __init__(self, topleft: Tuple[float, float], width: int) -> None:
        TicTacToeBasicBoard.__init__(self, topleft=topleft, width=width)

        cell_width = (width * (1-TicTacToeBoard.cell_dist_pct)) // 3
        cell_dist = (width * TicTacToeBoard.cell_dist_pct) // 4

        self.big_cell = TicTacToeCell(
            topleft=(cell_dist + topleft[0], cell_dist + topleft[1]),
            width=(3 * cell_width + 2 * cell_dist)
        )
        self.board = [
            TicTacToeCell(
                topleft=(
                    cell_dist + topleft[0] + (i % 3)*(cell_width+cell_dist),
                    cell_dist + topleft[1] + (i//3)*(cell_width+cell_dist)
                ),
                width=cell_width
            )
            for i in range(9)
        ]

    def update(self, state: int, cell: Optional[int] = None) -> None:

        if cell is None:
            if state in (-1, 0):
                for _cell in self.board:
                    _cell.update(state=state)
            else:
                raise ValueError("wrong value for board availability")
        else:
            if state in (1, 2):
                self.board[cell].update(state=state)
            else:
                raise ValueError("wrong value for the cell state in the board")

    def draw(self, screen: pygame.Surface) -> None:

        if self.big_cell.winner():
            self.big_cell.draw(screen)
        else:
            for cell in self.board:
                cell.draw(screen)


