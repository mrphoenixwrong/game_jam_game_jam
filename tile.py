import pygame

class Tile:
    def __init__(self, image, coordinates, collision):
        self.image = pygame.image.load(f"images\\{image}.png")
        self.rect = self.image.get_rect()
        self.x = coordinates[0]
        self.y = coordinates[1]

        self.rect.topleft = (self.x, self.y)

        self.collision = collision