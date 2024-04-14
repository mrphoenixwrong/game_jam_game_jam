import pygame
import os
from random import randint, choice
from lists import *

class Food:
    def __init__(self):
        self.type = choice(ORDERS)
        self.hot = choice(HEAT)

        self.image = pygame.image.load(os.path.join('images\\food', f'{self.type}_{self.hot}.png'))