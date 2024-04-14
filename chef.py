import pygame, os


class Chef:  

    def __init__(self,coordinates):
        self.frame = 1
        self.image = pygame.image.load(os.path.join("images\\chef", f"chefWalk{self.frame}.png"))
        self.rect = self.image.get_rect()

        self.collision_rect = pygame.surface.Surface((40, 40)).get_rect()

        self.x = coordinates[0]
        self.y = coordinates[1]

        self.rect.topleft = (self.x, self.y)
        self.collision_rect.topleft = (self.x, self.y + 40)
        self.direction = "none"

    def switch_image(self):
        if self.frame == 1:
            self.frame = 2
        else:
            self.frame = 1
        self.image = pygame.image.load(os.path.join("images\\chef", f"chefWalk{self.frame}.png"))


    def move(self, dt):
        if self.direction == "right":
            self.rect.x += 0.1 * dt
            self.collision_rect.x += 0.1 * dt
        elif self.direction == "left":
           self.rect.x -= 0.10 * dt
           self.collision_rect.x -= 0.1 * dt