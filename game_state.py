# -*- coding: utf-8 -*-
import sys
import game.mygym as gym
from constants import VISUAL
from constants import ACTION_SIZE


class GameState(object):
    def __init__(self, rand_seed, display=False, no_op_max=7):
        self.env = gym.make(visual=VISUAL, game='MatWorld')
        self.state_size = self.env.observation_space_shape
        self.action_size = len(self.env.action_space)

        self._no_op_max = no_op_max

        if display:
            self._setup_display()
        self.reset()

    def _process_frame(self, action):
        x_t, reward, terminal, total_reward = self.env.step(action)
        return reward, terminal, x_t

    def _setup_display(self):
        if sys.platform == 'darwin':
            import pygame
            pygame.init()

    def reset(self):
        x_t = self.env.reset()
        # _, _, x_t = self._process_frame(0)

        self.reward = 0
        self.terminal = False
        self.s_t = x_t  # np.stack((x_t, x_t, x_t, x_t), axis=1)

    def process(self, action):
        # convert original 18 action index to minimal action set index
        # real_action = self.real_actions[action]

        r, t, x_t1 = self._process_frame(action)

        self.reward = r
        self.terminal = t
        self.s_t1 = x_t1  # np.append(self.s_t[:, 1:], x_t1, axis=1)

    def update(self):
        self.s_t = self.s_t1
