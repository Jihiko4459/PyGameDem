
import sys

import pygame


# Инициализировать игру
pygame.init()

# инициализируйте микшер для воспроизведения звука
pygame.mixer.init()
pygame.mixer.music.load("res/sound.mp3")

# Создать экран
screen=pygame.display.set_mode((320,240))
WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)

HelloWorldColors=[BLACK, RED]

IMAGE=pygame.image.load("res/koshkaHelloWorld.png")
IMAGE_SMALL = pygame.transform.scale(IMAGE, (32, 32))

# Создать объект шрифта
font=pygame.font.Font(None, 32)

time=pygame.time

mouse_pos=None
count=0
oneSecondMarkReached=False
lastTime=0
while True:
    if oneSecondMarkReached:
        count=count+1



    screen.fill(WHITE) # заполнить фон

    #проверить событие выхода
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()


    #создать текстовую поверхность
    text=font.render("Hello World", True,
                     HelloWorldColors[count%2])


    # объемный текст с черной прямоугольной рамкой
    pygame.draw.rect(screen, BLACK, ((screen.get_width() -
                        text.get_width())/2-10,
                       (screen.get_height()-text.get_height())/2-10,
                                     text.get_width()+20,
                                     text.get_height()+20),1)


    # нарисуйте изображение над рамкой размером 32*32
    if mouse_pos!=None:
        screen.blit(IMAGE_SMALL,
                    (mouse_pos[0]-16, mouse_pos[1]-16))
    else:
        screen.blit(IMAGE_SMALL,
                    (screen.get_width() / 2 - 16,
                     (screen.get_height()
                      - text.get_height()) / 2 - 60))

    # переместить текстовую поверхность в центр экрана
    screen.blit(text, ((screen.get_width() -
                        text.get_width()) / 2,
                       (screen.get_height() - text.get_height()) / 2))

    # подавать звуковой сигнал
    if oneSecondMarkReached:
        pygame.mixer.music.play()

    #обновите экран
    pygame.display.flip()

    #сбросить флаг oneSecondMarkReached
    oneSecondMarkReached=False

    #информировать программу каждый раз, когда достигается
    #1-секундная отметка


    currentTime=time.get_ticks()
    if currentTime-lastTime>1000:
        lastTime=currentTime
        oneSecondMarkReached=True



