import pygame, os

class Player:
    def __init__(self, coordinates, has_plate):
        self.image = pygame.image.load(os.path.join('images', 'player.png'))
        self.rect = self.image.get_rect()

        self.x = coordinates[0]
        self.y = coordinates[1]

        self.rect.topleft = (self.x, self.y)

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