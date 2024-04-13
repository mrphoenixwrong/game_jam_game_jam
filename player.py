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

    #managing collision with other "people"
    def collision_up(self, other, distance):
        if pygame.Rect.colliderect(other.rect, self.rect) == True:
            self.rect.y += distance 
            print("touch")
            print(self.rect.x, self.rect.y)

    def collision_down(self, other, distance):
        if pygame.Rect.colliderect(other.rect, self.rect) == True:
            self.rect.y -= distance 
            print("touch")
            print(self.rect.x, self.rect.y)

    def collision_left(self, other, distance):
        if pygame.Rect.colliderect(other.rect, self.rect) == True:
            self.rect.x += distance 
            print("touch")
            print(self.rect.x, self.rect.y)

    def collision_right(self, other, distance):
        if pygame.Rect.colliderect(other.rect, self.rect) == True:
            self.rect.x -= distance 
            print("touch")
            print(self.rect.x, self.rect.y)


    def pick_up_or_put_down(self):
        if self.has_plate:
            self.has_plate = True
        else:
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
        else:
            if self.walking:
                data = data + "_walk"
                if self.has_plate:
                    data = data + "_plate"
            self.image = pygame.transform.flip(pygame.image.load(os.path.join('images\\player', 'player.png')), True, False)
        self.walking = not self.walking