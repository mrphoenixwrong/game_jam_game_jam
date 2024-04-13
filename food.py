import pygame
import os
from random import randint, choice
from lists import *

class Food:
    def __init__(self, type):
        self.type = type

        self.image = pygame.image.load(os.path.join('images', f'{type}.png'))
        self.rect = self.image.get_rect()