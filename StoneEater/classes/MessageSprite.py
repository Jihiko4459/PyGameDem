import pygame


class MessageSprite(pygame.sprite.Sprite):
    def __init__(self, message, x, y):
        super().__init__()
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        self.x = x
        self.y = y
        self.message = message
        self.small_font = pygame.font.Font(None, 36)
        self.image = self.small_font.render(message, True, BLACK)
        self.rect = self.image.get_rect().move(x, y)

    def update(self):
        BLACK = (0, 0, 0)
        self.image = self.small_font.render(self.message, True, BLACK)
        self.rect = self.image.get_rect().move(self.x, self.y)

    def update_message(self, message):
        self.message = message

    def draw(self, surface):
        surface.blit(self.image, self.rect)
