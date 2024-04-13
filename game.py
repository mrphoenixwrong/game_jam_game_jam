import pygame, os, json
from pygame.locals import *

from tile import Tile

pygame.init()

WIDTH, HEIGHT = 1000, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Jam Game")

TILE_SIZE = 50

rect = pygame.surface.Surface((50, 50))

class World:
    def __init__(self, world_data):
        self.tiles = []

        current_row = 0
        for row in world_data:
            current_col = 0
            for tile in row:
                if "floor" in tile:
                    img_rect = pygame.image.load(f"images\\{tile}.png").get_rect()
                    img_rect.topleft = (current_col * TILE_SIZE, current_row * TILE_SIZE)
                    tile = Tile(pygame.image.load(f"images\\{tile}.png"), img_rect, False)
                else:
                    img_rect = pygame.image.load(f"images\\{tile}.png").get_rect()
                    img_rect.topleft = (current_col * TILE_SIZE, current_row * TILE_SIZE)
                    tile = Tile(pygame.image.load(f"images\\{tile}.png"), img_rect, True)
                self.tiles.append(tile)
                current_col += 1
            current_row += 1

    def draw(self):
        for tile in self.tiles:
            window.blit(tile.image, tile.rect)


    def displayTiles(self):
        for tile in self.tiles:
            window.blit(tile[0], tile[1])

if os.path.exists('level_data.txt'):
    level_file = open('level_data.txt', 'r')
    world_data = json.load(level_file)
    world = World(world_data)
    RUNNING = True
else:
    RUNNING = False
    print("not all files downloaded :(")

clock = pygame.time.Clock()
while RUNNING:
    dt = clock.tick(60)
    window.fill((255,255,255))

    window.blit(rect, (0,0))
    world.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False

    key_pressed_is = pygame.key.get_pressed()
    
    if key_pressed_is[K_LEFT] or key_pressed_is[K_a]:
        pass
    if key_pressed_is[K_RIGHT] or key_pressed_is[K_d]:
        pass
    if key_pressed_is[K_UP] or key_pressed_is[K_w]:
        pass
    if key_pressed_is[K_DOWN] or key_pressed_is[K_s]:
        pass

    pygame.display.update()