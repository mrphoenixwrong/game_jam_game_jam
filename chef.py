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

    def cookin(self):
        direction = random.choice(["left", "right"])
        if direction == "right":
            pass
        else:
            pass

    def collision(self, other, distance):
        #if abs(self.rect.x) - abs(other.rect.x) < 0 and self.rect.y - other.rect.y < 0:
        if pygame.Rect.colliderect(self.rect, other.rect) == True:
            other.rect.x += 1 
            other.rect.y += 1
            print("touch")
            print(other.rect.x, other.rect.y)
