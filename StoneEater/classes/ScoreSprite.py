import pygame


class ScoreSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        BLACK = (0, 0, 0)
        self.score = 0
        self.small_font = pygame.font.Font(None, 16)
        #нужно исходное изображение для определения прямоугольника
        self.image = self.small_font.render(
            f'Score: {self.score}', True, BLACK)
        ## получить прямоугольник, ограничивающий счет
        self.rect = self.image.get_rect().move(0, 0)


    def update(self):
        BLACK = (0, 0, 0)
        self.image = self.small_font.render(
            f'Score: {self.score}', True, BLACK)
        # пересчитываем прямоугольник
        # так как изображение изменилось
        self.rect = self.image.get_rect().move(0, 0)

    def draw(self, surface):
        # Рисуем спрайт на экране
        surface.blit(self.image, self.rect)

    def update_score(self, score):
        self.score = score
