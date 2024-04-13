import pygame
import os
from random import choice
from lists import *

class NonPlayerCharacter:
    
    def __init__(self):
        self.image = pygame.image.load(os.path.join('images', 'npc.png'))
        self.rect = self.image.get_rect()

        self.rect.topleft = self.go_sit()
        self.order = self.make_order()

    # will use choice to pick a random key from the paths dictionary and go sit in the chair
    def go_sit(self):
        chair = choice(CHAIRS)
        index = CHAIRS.index(chair)
        CHAIRS.pop(index)
        return (chair[0]+5, chair[1]+5)

    # will use choice to pick from list of 3 foods , maybe start the timer too
    def make_order(self):
        self.anger = 0
        return choice(ORDERS)
    
    def karen(self):
        coordinates = self.rect.topleft

        self.image = pygame.image.load(os.path.join('images', 'mad_npc.png'))
        self.rect = self.image.get_rect()
        self.rect.topleft = coordinates

    # once the customer has its order it will wait for some time
    # IF it doesnt get its order Then it will get angry and leave
    # if the food gets cold and it didnt order cold food it wont take it (will have to trash)
    # if you take its order and dont give it their food in time it will get mad and disappear
