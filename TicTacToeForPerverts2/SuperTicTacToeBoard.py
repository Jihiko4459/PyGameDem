import pygame
import json
from typing import Tuple, Optional
from TicTacToeBoard import TicTacToeBoard
from TicTacToeBasicBoard import TicTacToeBasicBoard

#  Класс SuperTicTacToeBoard реализует функциональные возможности игры крестики-нолики 9 на 9.
#  Наследует функциональные возможности от базового класса TicTacToeBoard.
#  Атрибут board заполняется 9 досками для игры в крестики-нолики, каждая из которых содержит
#  локальная доска с 9 ячейками для игры в крестики-нолики.
class SuperTicTacToeBoard(TicTacToeBasicBoard):

    # Конструктор создает экземпляр класса SuperTicTacToeBoard с указанными параметрами
    def __init__(self,
                 topleft: Tuple[float, float],
                 width: int) -> None:
        # Инициализирует родительский класс
        TicTacToeBasicBoard.__init__(self, topleft=topleft, width=width)

        # определяет список из 9 локальных досок для моделирования сетки 3х3
        self.board = [
            TicTacToeBoard(
                topleft=(topleft[0] + (i % 3)*width/3,
                         topleft[1] + (i//3)*width/3),
                width=width//3
            )
            for i in range(9)
        ]

        # Определяет прямоугольник, чтобы нарисовать края глобальной сетки
        self.global_grid = pygame.Rect(self.topleft, (self.width, self.width))
        # устанавливаем цвет сетки
        self.edge_color =  [102, 0, 51]

    def update(self,
               state: int,
               local_board: Optional[int] = None,
               cell: Optional[int] = None) -> None:
        if local_board is None and cell is None:  # предоставляется только состояние
            # обновите состояние глобальной доски объявлений
            if state in (-1, 0):  # доступность глобальной доски
                for _local_board in self.board:
                    _local_board.update(state=state)
            else:  # состояние в (1,2) (победитель)
                raise ValueError("Победитель игры не может быть определен вручную")
        elif local_board is None and cell is not None:
            # ячейка указана, но ее местное правление отсутствует
            raise ValueError("Предоставьте местную доску для данной ячейки")
        else:
            self.board[local_board].update(state=state, cell=cell)
            if self.board[local_board].winner() > 0:
                # обновить победителя локальной доски
                self.board[local_board].big_cell.update(
                    state=self.board[local_board].winner())
            elif self.board[local_board].winner() == -1:  # нет победителя
                # обновите состояние всех ячеек локальной доски
                for _cell in self.board[local_board]:
                    _cell.reset()

    #Отображает глобальную доску на заданной поверхности.
    def draw(self, screen: pygame.Surface) -> None:
        # Draw the grid edges
        pygame.draw.rect(screen, color=self.edge_color, rect=self.global_grid)
        # Нарисуйте глобальную доску поверх сетки
        for local_board in self.board:
            local_board.draw(screen)


