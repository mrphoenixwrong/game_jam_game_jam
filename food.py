import pygame
import os
from random import randint, choice
from lists import *

class Food:
    def __init__(self):
        food = choice(ORDERS)
        self.type = food[0]
        self.price = food[1]
        self.hot = choice(HEAT)

        self.full_order = f"{self.type}_{self.hot}"
        self.prepare_time = 5

        self.image = pygame.image.load(os.path.join('images\\food', f'{self.type}_{self.hot}.png'))
        self.rect = self.image.get_rect()

        self.hot_image = pygame.image.load(os.path.join('images\\food', f'{self.type}_hot.png'))
        self.hot_rect = self.hot_image.get_rect()

        self.cold_image = pygame.image.load(os.path.join('images\\food', f'{self.type}_cold.png'))
        self.cold_rect = self.cold_image.get_rect()

    def __str__(self):
        meal = self.full_order
        return meal