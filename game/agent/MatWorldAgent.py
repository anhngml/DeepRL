import cv2
import pygame
import random
from abc import ABCMeta, abstractmethod
import numpy as np
from collections import deque
import math

from game.env.border import Border
from game.env.object import Object
from game.env.stone import Stone
from game.env.background import Background
from game.env.target import Target
from game.agent.iagent import IAgent


class GridWorldAgent(pygame.sprite.Sprite, IAgent):
    def __init__(self, env, trainingMode=False, rootFol=''):
        super().__init__()
        self.env = env

        # Initialise attributes of the car.
        self.width = env.sprite_width
        self.height = env.sprite_height
        self.reward = 0
        self.finish = False
        self.trainingMode = trainingMode

        self.origImage = pygame.image.load(rootFol + "game/agent/resources/gridworld_agent.png").convert_alpha()
        self.image = self.rot_center(self.origImage, 0)

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = self.width
        self.rect.y = self.height
        self.direct = 2
        self.random_direct = 2
        self.Id = 0
        self.trajectory_length = 4
        self.recently_trajectory = deque([], maxlen=self.trajectory_length)
        self.targetsInfo = []

    @staticmethod
    def rot_center(image, angle):
        """rotate an image while keeping its center and size"""
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def moveRight(self, pixels):
        step_reward = 0
        self.rect.x += pixels
        hit, cols = self.env.check_col(self)
        if hit:
            if len(cols) < 1:
                step_reward = self.env.hit_obj_penalty
            else:
                for col in cols:
                    if isinstance(col, Target):
                        step_reward = self.env.hit_target_reward
                        self.finish = True
                    elif isinstance(col, Border) \
                            or isinstance(col, Stone) \
                            or isinstance(col, Object):
                        step_reward = self.env.hit_obj_penalty
            if not self.finish:
                self.rect.x -= pixels
        step_reward += self.env.walk_energy
        self.reward += step_reward
        self.image = self.rot_center(self.origImage, 0)
        self.direct = 2
        return not hit, step_reward

    def moveLeft(self, pixels):
        step_reward = 0
        self.rect.x -= pixels
        hit, cols = self.env.check_col(self)
        if hit:
            if len(cols) < 1:
                step_reward = self.env.hit_obj_penalty
            else:
                for col in cols:
                    if isinstance(col, Target):
                        step_reward = self.env.hit_target_reward
                        self.finish = True
                    elif isinstance(col, Border) \
                            or isinstance(col, Stone) \
                            or isinstance(col, Object):
                        step_reward = self.env.hit_obj_penalty
            if not self.finish:
                self.rect.x += pixels

        step_reward += self.env.walk_energy
        self.reward += step_reward

        self.image = self.rot_center(self.origImage, 180)
        self.direct = 4
        return not hit, step_reward

    def moveUp(self, pixels):
        step_reward = 0
        self.rect.y -= pixels
        hit, cols = self.env.check_col(self)
        if hit:
            if len(cols) < 1:
                step_reward = self.env.hit_obj_penalty
            else:
                for col in cols:
                    if isinstance(col, Target):
                        step_reward = self.env.hit_target_reward
                        self.finish = True
                    elif isinstance(col, Border) \
                            or isinstance(col, Stone) \
                            or isinstance(col, Object):
                        step_reward = self.env.hit_obj_penalty
            if not self.finish:
                self.rect.y += pixels
        step_reward += self.env.walk_energy
        self.reward += step_reward
        self.image = self.rot_center(self.origImage, 90)
        self.direct = 1
        return not hit, step_reward

    def moveDown(self, pixels):
        step_reward = 0
        self.rect.y += pixels
        hit, cols = self.env.check_col(self)
        if hit:
            if len(cols) < 1:
                step_reward = self.env.hit_obj_penalty
            else:
                for col in cols:
                    if isinstance(col, Target):
                        step_reward = self.env.hit_target_reward
                        self.finish = True
                    elif isinstance(col, Border) \
                            or isinstance(col, Stone) \
                            or isinstance(col, Object):
                        step_reward = self.env.hit_obj_penalty
            if not self.finish:
                self.rect.y -= pixels

        step_reward += self.env.walk_energy
        self.reward += step_reward
        self.image = self.rot_center(self.origImage, -90)
        self.direct = 3
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

    def update_targets_info(self):
        self.targetsInfo = []
        if len(self.env.all_targets) < 1:
            return
        for target in self.env.all_targets:
            c_x = self.rect.x + (self.env.sprite_width / 2)
            c_y = self.rect.y + (self.env.sprite_height / 2)
            t_cx = target.rect.x + (self.env.sprite_width / 2)
            t_cy = target.rect.y + (self.env.sprite_height / 2)
            pygame.draw.line(self.env.screen, (0, 255, 0), [c_x, c_y], [t_cx, t_cy], 1)
            distance = math.hypot((t_cx - c_x), (t_cy - c_y))
            angle = math.atan2(c_y - t_cy, c_x - t_cx)
            self.targetsInfo.append([distance, angle])
            # print(self.targetsInfo)

    def observation(self, surface, view_range=5):
        self.update_targets_info()
        res = np.zeros((view_range, view_range))
        cols = (view_range - 1)/2
        x0 = self.rect.x - cols*self.env.sprite_width
        y0 = self.rect.y - cols*self.env.sprite_height
        for i in range(view_range):
            for j in range(view_range):
                xk = x0 + i*self.env.sprite_width
                yk = y0 + j*self.env.sprite_height
                sprites = list(filter(lambda e: e.rect.x == xk and e.rect.y == yk, self.env.all_sprites))
                sprite = sprites[len(sprites)-1] if len(sprites) > 0 else None
                val = 0
                if isinstance(sprite, Background):
                    val = 1
                elif isinstance(sprite, Stone):
                    val = 2
                elif isinstance(sprite, Target):
                    val = 3
                res[j, i] = val
        self.recently_trajectory.append(res)
        while len(self.recently_trajectory) < self.recently_trajectory.maxlen:
            self.recently_trajectory.append(res)
        result = np.array(list(self.recently_trajectory))
        result = np.reshape(result, view_range*view_range*self.trajectory_length)
        result = np.concatenate([result, np.array(self.targetsInfo).flatten()])
        # print(result)
        return result

    def move(self, direct):
        try:
            if self.finish:
                return True, 0
            if direct == 1:
                return self.moveUp(self.height)
            elif direct == 2:
                return self.moveRight(self.width)
            elif direct == 3:
                return self.moveDown(self.width)
            elif direct == 4:
                return self.moveLeft(self.height)
        except Exception as e:
            print("Error!!!!!!!!")
            print(direct)
            print(self.finish)

            print(e)

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
