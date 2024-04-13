import pygame, os

class Player:
    def __init__(self, coordinates, speed, has_plate):
        self.image = pygame.image.load(os.path.join('images', 'player.png'))
        self.rect = self.image.get_rect()

        self.x = coordinates[0]
        self.y = coordinates[1]

        self.collision_rect = pygame.surface.Surface((40, 40)).get_rect()

        self.rect.topleft = (self.x, self.y)
        self.collision_rect.topleft = (self.x, self.y+40)

        self.facing = "left"
        self.walking = False
        self.speed = speed
        self.has_plate = has_plate

    def pick_up_or_put_down(self):
        if self.has_plate:
            self.has_plate = True
        else:
            self.has_plate = False

    def turn(self):
        if self.facing == "left":
            self.image = pygame.transform.flip(pygame.image.load(os.path.join('images', 'player.png')), True, False)
            self.facing = "right"
        else:
            self.image = pygame.image.load(os.path.join('images', 'player.png')), True, False
            self.facing = "left"

    def walk(self):
        if self.facing == "left":
            if self.walking:
                self.image = pygame.image.load(os.path.join('images', 'player_walk.png'))
                self.walking = False
            else:
                self.image = pygame.image.load(os.path.join('images', 'player.png'))
                self.walking = True
        else:
            if self.walking:
                self.image = pygame.transform.flip(pygame.image.load(os.path.join('images', 'player_walk.png')), True, False)
                self.walking = False
            else:
                self.image = pygame.transform.flip(pygame.image.load(os.path.join('images', 'player.png')), True, False)
                self.walking = True