import sys
from math import gamma

import pygame

# инициализировать игру
pygame.init()

# создание экрана
gamewindow=pygame.display.set_mode((320,240))

WHITE=(255, 255, 255)

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()
    gamewindow.fill(WHITE)
    pygame.display.flip()
