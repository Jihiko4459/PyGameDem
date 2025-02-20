import pygame


# Create the sprite


class StoneSprite(pygame.sprite.Sprite):
    def __init__(self, color, row, column, piece_size, gem_value):
        super().__init__()
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        small_font = pygame.font.Font(None, 16)

        self.row = row
        self.column = column

        self.piece_size = piece_size
        #Создаём поверхность для спрайта
        self.image = pygame.Surface([piece_size, piece_size])
        self.image.fill(WHITE)
        # Рисуем прямоугольник на поверхности спрайта
        pygame.draw.circle(self.image, color, (piece_size/2,
                           piece_size/2), int(piece_size/2.2))
        self.gem_value = small_font.render(str(gem_value), True, WHITE)
        self.image.blit(self.gem_value, (piece_size/3, piece_size/4))
        self.rect = self.image.get_rect().move(column*piece_size, row*piece_size)

    def update(self):
        pass

    #  Рисуем спрайт на экране

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        surface.blit(self.gem_value, self.rect)
