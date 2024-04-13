import pygame, os, json
from pygame.locals import *

from tile import Tile
from player import Player

pygame.init()

WIDTH, HEIGHT = 1000, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Jam Game")

TILE_SIZE = 50

class World:
    def __init__(self, world_data):
        self.tiles = []

        current_row = 0
        for row in world_data:
            current_col = 0
            for tile in row:
                if "floor" in tile:
                    tile = Tile(tile, (current_col * TILE_SIZE, current_row * TILE_SIZE), False)
                else:
                    tile = Tile(tile, (current_col * TILE_SIZE, current_row * TILE_SIZE), True)
                self.tiles.append(tile)
                current_col += 1
            current_row += 1

    def displayTiles(self):
        for tile in self.tiles:
            window.blit(tile.image, tile.rect)

def createWorld():
    if os.path.exists('level_data.txt'):
        world_data = json.load(open('level_data.txt', 'r'))
        world = World(world_data)
        RUNNING = True
    else:
        RUNNING = False
    return world, RUNNING

clock = pygame.time.Clock()


def game_loop():
    world, RUNNING = createWorld()
    player = Player((850,450), False)

    while RUNNING:
        dt = clock.tick(60)

        world.displayTiles()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False

        key_pressed_is = pygame.key.get_pressed()
        
        if key_pressed_is[K_LEFT] or key_pressed_is[K_a]:
            player.rect.x -= 0.3 * dt
        if key_pressed_is[K_RIGHT] or key_pressed_is[K_d]:
            player.rect.x += 0.3 * dt
        if key_pressed_is[K_UP] or key_pressed_is[K_w]:
            player.rect.y -= 0.3 * dt
        if key_pressed_is[K_DOWN] or key_pressed_is[K_s]:
            player.rect.y += 0.3 * dt

        # Collision Detection
        for tile in world.tiles:
            # Collide with left side of tile
            if player.rect.collidepoint((tile.x, tile.y + TILE_SIZE/2)) and tile.collision:
                player.rect.x = tile.x - TILE_SIZE
            # Collide with right side of tile
            if player.rect.collidepoint((tile.x + TILE_SIZE, tile.y + TILE_SIZE/2)) and tile.collision:
                player.rect.x = tile.x + TILE_SIZE
            # Collide with top of tile
            if player.rect.collidepoint((tile.x + TILE_SIZE/2, tile.y)) and tile.collision:
                player.rect.y = tile.y - TILE_SIZE
            # Collide with bottom of tile
            if player.rect.collidepoint((tile.x + TILE_SIZE/2, tile.y + TILE_SIZE)) and tile.collision:
                player.rect.y = tile.y + TILE_SIZE

            # Collide with topleft side of tile
            if player.rect.collidepoint((tile.x, tile.y)) and tile.collision:
                #  Player distance left > Player distance top
                if tile.x - player.rect.x > tile.y - player.rect.y:
                    player.rect.x = tile.x - TILE_SIZE
                else:
                    player.rect.y = tile.y - TILE_SIZE
            # Collide with topright side of tile
            if player.rect.collidepoint((tile.x + TILE_SIZE - 1, tile.y)) and tile.collision:
                #  Player distance right > Player distance top
                if player.rect.x - tile.x > tile.y - player.rect.y:
                    player.rect.x = tile.x + TILE_SIZE
                else:
                    player.rect.y = tile.y - TILE_SIZE
            # Collide with bottomleft of tile
            if player.rect.collidepoint((tile.x, tile.y + TILE_SIZE - 1)) and tile.collision:
                #  Player distance left > Player distance bottom
                if tile.x - player.rect.x > player.rect.y - tile.y:
                    player.rect.x = tile.x - TILE_SIZE
                else:
                    player.rect.y = tile.y + TILE_SIZE
            # Collide with bottomright of tile
            if player.rect.collidepoint((tile.x + TILE_SIZE - 1, tile.y + TILE_SIZE - 1)) and tile.collision:
                #  Player distance right > Player distance bottom
                if player.rect.x - tile.x > player.rect.y - tile.y:
                    player.rect.x = tile.x + TILE_SIZE
                else:
                    player.rect.y = tile.y + TILE_SIZE

        window.blit(player.image, player.rect)

        pygame.display.update()

game_loop()