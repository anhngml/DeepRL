import pygame, pytmx


class Object(pygame.sprite.Sprite):
    def __init__(self, env, x, y, img):
        super().__init__()
        self.env = env
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x * env.sprite_width
        self.rect.y = y * env.sprite_height
        self.mask = pygame.mask.from_surface(self.image)
