import pygame, pytmx


class Target(pygame.sprite.Sprite):
    def __init__(self, env, x, y, img=None):
        super().__init__()
        self.env = env
        if img is None:
            img = pygame.image.load(env.RootFol + "game/env/map/resources/gridworld/target.png").convert_alpha()
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = x * env.sprite_width
        self.rect.y = y * env.sprite_height
        self.mask = pygame.mask.from_surface(self.image)
