from pytmx.util_pygame import load_pygame
import pygame
from game.env.stone import Stone
from game.env.border import Border
from game.env.object import Object
from game.env.target import Target
from game.env.ienv import IEnv


class CDEnv(IEnv):

    def __init__(self, rootFol=''):
        tiled_map = load_pygame(rootFol + 'game/env/map/resources/cdgame/map.tmx', invert_y=True)
        assert isinstance(tiled_map, object)
        self.gameMap = tiled_map
        self.all_sprites = pygame.sprite.Group()
        self.sprite_width = 32
        self.sprite_height = 32

        self.hit_target_reward = 200
        self.hit_obj_penalty = -1
        self.walk_energy = -0.01

    def refresh(self, background):
        self.all_sprites = pygame.sprite.Group()
        # draw map data on screen
        for layer in self.gameMap.visible_layers:
            for x, y, gid, in layer:
                tile = self.gameMap.get_tile_image_by_gid(gid)
                # print(layer.name)
                if tile is not None:
                    if layer.name == 'stone':
                        # print(layer.name)
                        self.all_sprites.add(Stone(self, x, y, tile))
                    elif layer.name == 'border':
                        # print(layer.name)
                        self.all_sprites.add(Border(self, x, y, tile))
                    elif layer.name == 'object':
                        # print(layer.name)
                        self.all_sprites.add(Object(self, x, y, tile))
                    elif layer.name == 'target':
                        self.all_sprites.add(Target(self, x, y, tile))

                    background.blit(tile, (x * self.gameMap.tilewidth, y * self.gameMap.tileheight))

    @staticmethod
    def check_col(rect1, rect2):
        return rect2.x + rect2.width > rect1.x > rect2.x - rect2.width and \
               rect2.y + rect2.height > rect1.y > rect2.y - rect2.height

    def check_col(self, sprite):
        all_cols = pygame.sprite.spritecollide(sprite, self.all_sprites, False, pygame.sprite.collide_mask)
        for s in all_cols:
            if isinstance(s, Target):
                sprite.finish = True
        return len(all_cols) > 0, all_cols

    def Capture(self, display, name, pos, size):  # (pygame Surface, String, tuple, tuple)
        image = pygame.Surface(size)  # Create image surface
        image.blit(display, (0, 0), (pos, size))  # Blit portion of the display to the image
        pygame.image.save(image, name)  # Save the image to the disk
        # Capture(display, "Capture.png", (50, 50), (100, 100))