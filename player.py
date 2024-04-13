import pygame, os

class Player:
    def __init__(self, coordinates, speed, has_plate):
        self.image = pygame.image.load(os.path.join('images', 'player.png'))
        self.rect = self.image.get_rect()

        self.collision_box = pygame.surface.Surface((40, 40))
        self.collision_rect = self.collision_box.get_rect()

        self.x = coordinates[0]
        self.y = coordinates[1]

        self.rect.topleft = (self.x, self.y)
        self.collision_rect.topleft = (self.x, self.y + 40)

        self.speed = speed
        self.has_plate = has_plate

    def pick_up_or_put_down(self):
        if self.has_plate:
            self.has_plate = True
        else:
            self.has_plate = False