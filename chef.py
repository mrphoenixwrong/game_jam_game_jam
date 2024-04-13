import pygame, random


class Chef:  

    def __init__(self,coordinates):
        miku = pygame.image.load("unused sprites/mikudayo.png")
        self.image = pygame.transform.scale(miku, (60,80))
        #self.image = pygame.image.load(os.path.join('unused sprites', 'mikudayo.png'))
        self.rect = self.image.get_rect()


        #pygame.transform.scale(self.rect, (40,40))
        self.x = coordinates[0]
        self.y = coordinates[1]

        self.rect.topleft = (self.x, self.y)


    def cookin(self, direction: str):
        if direction == "right":
            self.rect.x += .5
        else:
           self.rect.x -= .5
           