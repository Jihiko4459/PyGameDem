import pygame


class TimeSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        BLACK = (0, 0, 0)
        self.time = 0
        self.small_font = pygame.font.Font(None, 16)
        self.image = self.small_font.render(f'Time: {self.time}', True, BLACK)
        self.rect = self.image.get_rect().move(280, 15)

    def update(self):
        BLACK = (0, 0, 0)
        #обновить изображение времени
        self.image = self.small_font.render(f'Time: {self.time}', True, BLACK)
        self.rect = self.image.get_rect().move(280, 15)

    def draw(self, surface):
        #рисуем время на экране
        surface.blit(self.image, self.rect)

    def update_time(self, time_limit, time_in_milliseconds):
        #рассчитать оставшееся время
        calculated_time = int(time_limit - (time_in_milliseconds / 1000))
        #не нужно опускаться ниже 0
        if calculated_time < 0:
            calculated_time = 0
        self.time = calculated_time
