import json
import pygame
from typing import Tuple

# Класс TicTacToeCell определяет ячейку на доске в виде крестиков.
# На обычной доске для игры в крестики-нолики есть 9 ячеек. Каждый из них может быть заполнен
# только одним из двух игроков во время игры. Ячейка может быть заполнена
# только в том случае, если он доступен. После того, как игрок заполнит ячейку, в ней
# появится победитель, и она больше не будет доступна и не может быть заполнена повторно.
# Этот класс предназначен для использования на доске для игры в крестики-нолики
# класс, определяющий поведение ячеек и логику игры.
class TicTacToeCell:

    def __init__(self,
                 topleft: Tuple[float, float],
                 width: int
                 ) -> None:

        self.width = width
        self._winner = 0
        self.available = True

        self._available_bg_color = [255, 102, 178]
        self._unavailable_bg_color = [255, 204, 229]
        player1_img = pygame.image.load("images/player1.jpg").convert()
        self._player1_img = pygame.transform.scale(player1_img, (width, width))
        player2_img = pygame.image.load("images/player2.jpg").convert()
        self._player2_img = pygame.transform.scale(player2_img, (width, width))

        self._image = pygame.Surface([self.width, self.width])
        self._rect = self._image.get_rect(topleft=topleft)

    def winner(self) -> int:

        return self._winner

    def update(self, state: int) -> None:

        if state == -1:
            self.available = False
        elif state == 0:
            self.available = True
        elif state in (1, 2):
            self._winner = state
        else:
            raise ValueError("неверное значение для состояния ячейки")

    def draw(self, screen: pygame.Surface) -> None:
        if self._winner:
            img = self._player1_img if self._winner == 1 else self._player2_img
            self._image = img
        else:
            if self.available:
                bg_color = self._available_bg_color
            else:
                bg_color = self._unavailable_bg_color
            self._image.fill(bg_color)
        screen.blit(self._image, self._rect)

    def collidepoint(self, point: Tuple[float, float]) -> bool:

        return self._rect.collidepoint(point)

    def reset(self) -> None:

        self._winner = 0

