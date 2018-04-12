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
    def __init__(self, env, trainingMode=False, rootFol=''): raise NotImplementedError

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

    @abstractmethod
    def observation(self, surface, view_range=5): raise NotImplementedError