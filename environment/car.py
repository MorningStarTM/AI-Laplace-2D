import pygame
import math
import random
from utils import blit_rotate_center


class AbstractCar:
    """
    Base class for Car
    """
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel


    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)


