import cv2
import pygame
import random
from abc import ABCMeta, abstractmethod

from game.env.border import Border
from game.env.object import Object
from game.env.stone import Stone
from game.env.target import Target


class IAgent:
    __metaclass__ = ABCMeta

    @classmethod
    def version(self): return "1.0"

    @abstractmethod
    def moveRight(self, pixels): raise NotImplementedError

    @abstractmethod
    def moveLeft(self, pixels): raise NotImplementedError

    @abstractmethod
    def moveUp(self, pixels): raise NotImplementedError

    @abstractmethod
    def moveDown(self, pixels): raise NotImplementedError

    @abstractmethod
    def move(self, direct): raise NotImplementedError

    @abstractmethod
    def random_walk(self): raise NotImplementedError

    @abstractmethod
    def updateReward(self, font, screen): raise NotImplementedError

    @abstractmethod
    def firstView(self, surface, view_range=5): raise NotImplementedError


class Agent(pygame.sprite.Sprite, IAgent):
    def __init__(self, env, trainingMode=False, rootFol=''):
        super().__init__()
        self.env = env

        # Initialise attributes of the car.
        self.width = env.sprite_width
        self.height = env.sprite_height
        self.reward = 0
        self.finish = False
        self.trainingMode = trainingMode

        self.image = pygame.image.load(rootFol + "game/agent/resources/gridworld_agent.png").convert_alpha()

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = self.width
        self.rect.y = self.height
        self.direct = 2
        self.random_direct = 2
        self.Id = 0

    def moveRight(self, pixels):
        step_reward = 0
        self.rect.x += pixels
        hit, cols = self.env.check_col(self)
        if hit:
            for col in cols:
                if isinstance(col, Target):
                    step_reward = self.env.hit_target_reward
                    self.finish = True
                elif isinstance(col, Border) \
                        or isinstance(col, Stone) \
                        or isinstance(col, Object):
                    step_reward = self.env.hit_obj_penalty
            self.rect.x -= pixels
        step_reward += self.env.walk_energy
        self.reward += step_reward
        if self.direct == 4:
            self.image = pygame.transform.flip(self.image, True, False)
        self.direct = 2
        return not hit, step_reward

    def moveLeft(self, pixels):
        step_reward = 0
        self.rect.x -= pixels
        hit, cols = self.env.check_col(self)
        if hit:
            for col in cols:
                if isinstance(col, Target):
                    step_reward = self.env.hit_target_reward
                    self.finish = True
                elif isinstance(col, Border) \
                        or isinstance(col, Stone) \
                        or isinstance(col, Object):
                    step_reward = self.env.hit_obj_penalty
            self.rect.x += pixels

        step_reward += self.env.walk_energy
        self.reward += step_reward

        if self.direct == 2:
            self.image = pygame.transform.flip(self.image, True, False)
        self.direct = 4
        return not hit, step_reward

    def moveUp(self, pixels):
        step_reward = 0
        self.rect.y -= pixels
        hit, cols = self.env.check_col(self)
        if hit:
            for col in cols:
                if isinstance(col, Target):
                    step_reward = self.env.hit_target_reward
                    self.finish = True
                elif isinstance(col, Border) \
                        or isinstance(col, Stone) \
                        or isinstance(col, Object):
                    step_reward = self.env.hit_obj_penalty

            self.rect.y += pixels
        step_reward += self.env.walk_energy
        self.reward += step_reward
        return not hit, step_reward

    def moveDown(self, pixels):
        step_reward = 0
        self.rect.y += pixels
        hit, cols = self.env.check_col(self)
        if hit:
            for col in cols:
                if isinstance(col, Target):
                    step_reward = self.env.hit_target_reward
                    self.finish = True
                elif isinstance(col, Border) \
                        or isinstance(col, Stone) \
                        or isinstance(col, Object):
                    step_reward = self.env.hit_obj_penalty

            self.rect.y -= pixels

        step_reward += self.env.walk_energy
        self.reward += step_reward
        return not hit, step_reward

    def updateReward(self, font, screen):
        if self.finish:
            textsurface = font.render('total rwd: {}'.format(round(self.reward, 2)), True, (255, 0, 0))
        else:
            textsurface = font.render('reward: {}'.format(round(self.reward, 2)), True, (255, 0, 0))
        screen.blit(textsurface, (205, 0))

    def firstView(self, surface, view_range=5):
        im = pygame.Surface((self.env.sprite_width * view_range, self.env.sprite_height * view_range))
        im.blit(surface, (0, 0),
                ((self.rect.x - ((view_range - 1) / 2) * self.env.sprite_width,
                  self.rect.y - ((view_range - 1) / 2) * self.env.sprite_height),
                 (self.env.sprite_width * view_range, self.env.sprite_height * view_range)))

        img = pygame.surfarray.array3d(im)
        img = img.swapaxes(0, 1)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        return img

    def move(self, direct):
        if self.finish:
            return
        if direct == 1:
            return self.moveUp(32)
        elif direct == 2:
            return self.moveRight(32)
        elif direct == 3:
            return self.moveDown(32)
        elif direct == 4:
            return self.moveLeft(32)

    def random_walk(self):
        if self.finish:
            return
        success, reward = self.move(self.random_direct)
        if not success:
            ran = random.randint(1, 4)
            while ran == self.random_direct:
                ran = random.randint(1, 4)
            self.random_direct = ran
        else:
            p = random.randint(1, 101)
            if p > 95:
                self.random_direct = random.randint(1, 4)

    # def checkCol(self, dx, dy):
    #     all_cols = pygame.sprite.spritecollide(self, self.env.all_sprites, False, pygame.sprite.collide_mask)
    #     print(all_cols)
    #     return len(all_cols) > 0
    #
    #     for layer in self.env.gameMap.visible_layers:
    #         if isinstance(layer, pytmx.TiledTileLayer):
    #             if layer.name == "stone" or layer.name == "border" or layer.name == 'object':
    #                 for x, y, img in layer.tiles():
    #                     map_mask = pygame.mask.from_surface(img)
    #                     if pygame.sprite.spritecollide(self.mask, map_mask, False, pygame.sprite.collide_mask):
    #                         print("You hit the " + layer.name)
    #                         return True
    #
    #                     if self.env.check_col(
    #                             pygame.Rect(self.rect.x + dx, self.rect.y + dy, self.rect.width, self.rect.height),
    #                             pygame.Rect(x*64, y*64, 64, 64)) is True:
    #                         print("You hit the " + layer.name)
    #                         return True
    #     return False
