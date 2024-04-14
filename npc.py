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

        self.chair = choice(CHAIRS)
        index = CHAIRS.index(self.chair)
        CHAIRS.pop(index)
        if self.chair[2] == "Right":
            self.default_image = f"{self.character}Side"
            self.image = pygame.transform.flip(pygame.image.load(os.path.join(f'images\\NPCs\\{self.character}', f'{self.default_image}.png')), True, False)
        else:
            if self.chair[2] == "Left":
                self.default_image = f"{self.character}Side"
            else:
                self.default_image = f"{self.character}{self.chair[2]}"
            self.image = pygame.image.load(os.path.join(f'images\\NPCs\\{self.character}', f'{self.default_image}.png'))
        self.rect = self.image.get_rect()

        self.collision_rect = pygame.surface.Surface((40, 40)).get_rect()

        self.rect.topleft = (self.chair[0], self.chair[1]-40)
        self.collision_rect.topleft = (self.chair[0]+5, self.chair[1]+5)



    def ready_to_order(self, can_cold):
        self.order_status = "ready to order"
        self.anger = 10

        self.order = Food(can_cold)

        self.thought_image = pygame.image.load(os.path.join('images\\food', 'thought_bubble.png'))
        self.thought_rect = self.thought_image.get_rect()

        self.thought_rect.center = (self.rect.right, self.rect.top - 15)

    # will use choice to pick from list of 3 foods , maybe start the timer too
    def order_taken(self):
        self.order_status = "waiting for food"
        self.anger = 15

        self.food_image = pygame.image.load(os.path.join('images\\food', f'{self.order.type}_{self.order.hot}.png'))
        self.food_rect = self.food_image.get_rect()

        self.food_rect.center = (self.thought_rect.centerx, self.thought_rect.centery - 3)

    def received_order(self):
        self.order_status = "order complete"
        self.leaving = 5
        return self.order.price

    def karen(self):
        self.order_status = "too late!"
        self.leaving = 5

        coordinates = self.rect.topleft

        if self.chair[2] == "Right":
            self.image = pygame.transform.flip(pygame.image.load(os.path.join(f'images\\NPCs\\{self.character}', f'{self.default_image}Angry.png')), True, False)
        else:
            self.image = pygame.image.load(os.path.join(f'images\\NPCs\\{self.character}', f'{self.default_image}Angry.png'))
        self.rect = self.image.get_rect()
        self.rect.topleft = coordinates
    
    def stand_up(self):
        CHAIRS.append(self.chair)

    # once the customer has its order it will wait for some time
    # IF it doesnt get its order Then it will get angry and leave
    # if the food gets cold and it didnt order cold food it wont take it (will have to trash)
    # if you take its order and dont give it their food in time it will get mad and disappear
