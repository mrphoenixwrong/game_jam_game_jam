import pygame, random


class Chef:  

    def __init__(self,coordinates):
        miku = pygame.image.load("images/chef/chefCook1.png")
        self.image = pygame.transform.scale(miku, (50,75))
        self.img_rect = self.image.get_rect()
        self.rect = pygame.surface.Surface((50, 60)).get_rect()

        self.collision_rect = pygame.surface.Surface((40, 40)).get_rect()

        self.x = coordinates[0]
        self.y = coordinates[1]

        self.rect.topleft = (self.x, self.y)
        self.collision_rect.topleft = (self.x, self.y + 40)


    def cookin(self, direction: str):
        if direction == "right":
            self.rect.x += 2
            self.img_rect.x += 2
        else:
           self.rect.x -= 2
           self.img_rect.x -= 2
