import cv2
import pygame
import random
from abc import ABCMeta, abstractmethod

from game.env.border import Border
from game.env.object import Object
from game.env.stone import Stone
from game.env.target import Target


class IEnv:
    __metaclass__ = ABCMeta

    @classmethod
    def version(self): return "1.0"

    @abstractmethod
    def __init__(self, rootFol=''): raise NotImplementedError

    @abstractmethod
    def refresh(self, background): raise NotImplementedError

    @abstractmethod
    def check_col(self, sprite): raise NotImplementedError
