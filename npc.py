import pygame
import os
from random import choice
from chair_locations import places

class NonPlayerCharacter:
    
    def __init__(self, coordinates, order):
        self.image = pygame.image.load(os.path.join('images', 'player.png'))
        self.rect = self.image.get_rect()

        self.x = coordinates[0]
        self.y = coordinates[1]

        self.rect.topleft = (self.x, self.y)

        self.order = order

    # will use choice to pick a random key from the paths dictionary and go sit in the chair
    def go_sit(self):
        (self.x, self.y) = choice(places)

    # will use choice to pick from list of 3 foods , maybe start the timer too
    def make_order(self):
        pass

    # once the customer has its order it will wait for some time
    # IF it doesnt get its order Then it will get angry and leave
    # if the food gets cold and it didnt order cold food it wont take it (will have to trash)
    # if you take its order and dont give it their food in time it will get mad and disappear
