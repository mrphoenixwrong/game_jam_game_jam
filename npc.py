import pygame
import os
from random import randint, choice
from lists import CHAIRS, ORDERS, CHARACTERS

from food import Food

class NonPlayerCharacter:
    
    def __init__(self):
        self.character = choice(CHARACTERS)
        self.sit_down()

    # will use choice to pick a random key from the paths dictionary and go sit in the chair
    def sit_down(self):
        self.order_status = "just sat"
        self.anger = 999
        self.wait = randint(2,4)

        chair = choice(CHAIRS)
        index = CHAIRS.index(chair)
        CHAIRS.pop(index)
        if chair[2] == "Right":
            self.default_image = pygame.transform.flip(pygame.image.load(os.path.join('images\\NPCs', f'{self.character}Side.png')), True, False)
            self.rect = self.default_image.get_rect()
        elif chair[2] == "Left":
            self.default_image = pygame.image.load(os.path.join('images\\NPCs', f'{self.character}Side.png'))
            self.rect = self.default_image.get_rect()
        else:
            self.default_image = pygame.image.load(os.path.join('images\\NPCs', f'{self.character}{chair[2]}.png'))
            self.rect = self.default_image.get_rect()
        self.rect.topleft = (chair[0], chair[1]-40)

        self.image = self.default_image

    def ready_to_order(self):
        self.order_status = "ready to order"
        self.anger = 10

        coordinates = self.rect.topleft

        self.image = pygame.image.load(os.path.join('images\\NPCs', 'take_my_order!.png'))
        self.rect = self.image.get_rect()
        self.rect.topleft = coordinates

        self.order = Food()

        self.thought_image = pygame.image.load(os.path.join('images\\food', f'thought_bubble.png'))
        self.thought_rect = self.thought_image.get_rect()

        self.food_image = pygame.image.load(os.path.join('images\\food', f'{self.order.type}_{self.order.hot}.png'))
        self.food_rect = self.food_image.get_rect()

        self.thought_rect.center = (self.rect.centerx, self.rect.top - 15)
        self.food_rect.center = (self.rect.centerx, self.rect.top - 15)

    # will use choice to pick from list of 3 foods , maybe start the timer too
    def order_taken(self):
        self.order_status = "waiting for food"
        self.anger = 30

        coordinates = self.rect.topleft

        self.image = self.default_image
        self.rect = self.image.get_rect()
        self.rect.topleft = coordinates

    def received_order(self):
        self.order_status = "order complete"

    def karen(self):
        self.order_status = "too late!"
        self.angered = 5

        coordinates = self.rect.topleft

        self.image = pygame.image.load(os.path.join('images\\NPCs', 'mad_npc.png'))
        self.rect = self.image.get_rect()
        self.rect.topleft = coordinates
    
    def stand_up(self):
        CHAIRS.append((self.rect.left, self.rect.top))

    # once the customer has its order it will wait for some time
    # IF it doesnt get its order Then it will get angry and leave
    # if the food gets cold and it didnt order cold food it wont take it (will have to trash)
    # if you take its order and dont give it their food in time it will get mad and disappear
