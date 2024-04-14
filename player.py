import pygame, os

class Player:
    def __init__(self, coordinates, speed, has_plate):
        self.image = pygame.image.load(os.path.join('images\\player', 'player.png'))
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

    #player rect getter (pythonic)
    @property
    def rect(self):
        return self._rect
    
    @rect.setter
    def rect(self, new_rect):
        self._rect = new_rect
    

    #managing collision with other "people"
    def collision_up(self, other, distance):
        if pygame.Rect.colliderect(other.collision_rect, self.collision_rect):
            self.collision_rect.y += distance
            self.rect.y += distance

    def collision_down(self, other, distance):
        if pygame.Rect.colliderect(other.collision_rect, self.collision_rect):
            self.collision_rect.y -= distance
            self.rect.y -= distance 

    def collision_left(self, other, distance):
        if pygame.Rect.colliderect(other.collision_rect, self.collision_rect):
            self.collision_rect.x += distance
            self.rect.x += distance

    def collision_right(self, other, distance):
        if pygame.Rect.colliderect(other.collision_rect, self.collision_rect):
            self.collision_rect.x -= distance
            self.rect.x -= distance


    def pick_up(self):
        if not self.has_plate:
            self.has_plate = True
            self.freeze_timer = 5

    def put_down(self):
        if self.has_plate:
            self.has_plate = False

    def turn(self):
        if self.facing == "left":
            self.image = pygame.transform.flip(pygame.image.load(os.path.join('images\\player', 'player.png')), True, False)
            self.facing = "right"
        else:
            self.image = pygame.image.load(os.path.join('images\\player', 'player.png'))
            self.facing = "left"

    def walk(self):
        data = ""
        if self.facing == "left":
            if self.walking:
                data = data + "_walk"
            if self.has_plate:
                data = data + "_plate"
            self.image = pygame.image.load(os.path.join('images\\player', f'player{data}.png'))
        elif self.facing == "right":
            if self.walking:
                data = data + "_walk"
            if self.has_plate:
                data = data + "_plate"
            self.image = pygame.transform.flip(pygame.image.load(os.path.join('images\\player', f'player{data}.png')), True, False)
        self.walking = not self.walking