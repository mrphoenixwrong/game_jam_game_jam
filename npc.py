import pygame
import os
from random import randint, choice
from lists import *

class NonPlayerCharacter:
    
    def __init__(self):
        self.image = pygame.image.load(os.path.join('images', 'npc.png'))
        self.rect = self.image.get_rect()

        self.rect.topleft = self.sit_down()

    # will use choice to pick a random key from the paths dictionary and go sit in the chair
    def sit_down(self):
        self.order_status = "just sat"
        self.anger = 999
        self.wait = randint(2,4)

        chair = choice(CHAIRS)
        index = CHAIRS.index(chair)
        CHAIRS.pop(index)
        return (chair[0], chair[1])

    def ready_to_order(self):
        self.order_status = "ready to order"
        self.anger = 10

        coordinates = self.rect.topleft

        self.image = pygame.image.load(os.path.join('images', 'take_my_order!.png'))
        self.rect = self.image.get_rect()
        self.rect.topleft = coordinates

    # will use choice to pick from list of 3 foods , maybe start the timer too
    def order_taken(self):
        self.order_status = "waiting for food"
        self.anger = 30
        self.order = choice(ORDERS)

        coordinates = self.rect.topleft

        self.image = pygame.image.load(os.path.join('images', 'npc.png'))
        self.rect = self.image.get_rect()
        self.rect.topleft = coordinates

    def received_order(self):
        self.order_status = "order complete"

    def karen(self):
        self.order_status = "too late!"
        self.angered = 5

        coordinates = self.rect.topleft

        self.image = pygame.image.load(os.path.join('images', 'mad_npc.png'))
        self.rect = self.image.get_rect()
        self.rect.topleft = coordinates
    
    def stand_up(self):
        CHAIRS.append((self.rect.left, self.rect.top))

    # once the customer has its order it will wait for some time
    # IF it doesnt get its order Then it will get angry and leave
    # if the food gets cold and it didnt order cold food it wont take it (will have to trash)
    # if you take its order and dont give it their food in time it will get mad and disappear
