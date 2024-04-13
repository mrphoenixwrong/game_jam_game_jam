import pygame, os, json
from pygame.locals import *

from tile import Tile
from player import Player

pygame.init()

WIDTH, HEIGHT = 1000, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Jam Game")

TILE_SIZE = 50
PLAYER_SIZE = 40

class World:
    def __init__(self, world_data):
        self.tiles = []

        current_row = 0
        for row in world_data:
            current_col = 0
            for tile in row:
                if "floor" in tile or "chair" in tile:
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
            player.collision_rect.x -= 0.3 * dt
        if key_pressed_is[K_RIGHT] or key_pressed_is[K_d]:
            player.rect.x += 0.3 * dt
            player.collision_rect.x += 0.3 * dt
        if key_pressed_is[K_UP] or key_pressed_is[K_w]:
            player.rect.y -= 0.3 * dt
            player.collision_rect.y -= 0.3 * dt
        if key_pressed_is[K_DOWN] or key_pressed_is[K_s]:
            player.rect.y += 0.3 * dt
            player.collision_rect.y += 0.3 * dt

        # Collision Detection
        print(player.rect.topleft)
        print((player.collision_rect.left, player.collision_rect.top - 40))

        for tile in world.tiles:
            # SIDE COLLISIONS
            # Collide with left side of tile
            if player.collision_rect.collidepoint((tile.rect.left, tile.rect.centery)) and tile.collision:
                player.rect.x = tile.x - PLAYER_SIZE
                player.collision_rect.x = tile.x - PLAYER_SIZE
            # Collide with right side of tile
            if player.collision_rect.collidepoint((tile.rect.right, tile.rect.centery)) and tile.collision:
                player.rect.x = tile.x + TILE_SIZE
                player.collision_rect.x = tile.x + TILE_SIZE
            # Collide with top of tile
            if player.rect.collidepoint((tile.rect.centerx, tile.rect.top)) and tile.collision:
                player.rect.y = tile.y - PLAYER_SIZE * 2
                player.collision_rect.y = tile.y - PLAYER_SIZE
            # Collide with bottom of tile
            if player.collision_rect.collidepoint((tile.rect.centerx, tile.rect.bottom)) and tile.collision:
                player.rect.y = tile.y + TILE_SIZE - PLAYER_SIZE
                player.collision_rect.y = tile.y + TILE_SIZE

            # CORNER COLLISIONS
            # Collide with topleft side of tile
            if player.collision_rect.collidepoint(tile.rect.topleft) and tile.collision:
                # Pushing right = go left
                if tile.rect.left - player.collision_rect.left > tile.rect.top - player.collision_rect.top:
                    player.rect.right = tile.rect.left
                    player.collision_rect.right = tile.rect.left
                # Pushing down = go up
                if tile.rect.left - player.collision_rect.left < tile.rect.top - player.collision_rect.top:
                    player.rect.bottom = tile.rect.top 
                    player.collision_rect.bottom = tile.rect.top
            # Collide with topright of tile
            if player.collision_rect.collidepoint(tile.rect.topright) and tile.collision:
                # Pushing left = go right
                if player.collision_rect.right - tile.rect.right > tile.rect.top - player.collision_rect.top:
                    player.rect.left = tile.rect.right
                    player.collision_rect.left = tile.rect.right
                # Pushing down = go up
                if player.collision_rect.right - tile.rect.right < tile.rect.top - player.collision_rect.top:
                    player.rect.bottom = tile.rect.top
                    player.collision_rect.bottom = tile.rect.top
            # Collide with bottomleft of tile
            if player.collision_rect.collidepoint(tile.rect.bottomleft) and tile.collision:
                # Pushing right = go left
                if tile.rect.left - player.collision_rect.left > player.collision_rect.bottom - tile.rect.bottom:
                    player.rect.right = tile.rect.left
                    player.collision_rect.right = tile.rect.left
                # Pushing up = go down
                if tile.rect.left - player.collision_rect.left < player.collision_rect.bottom - tile.rect.bottom:
                    player.rect.top = tile.rect.bottom - PLAYER_SIZE
                    player.collision_rect.top = tile.rect.bottom
            # Collide with bottomright of tile
            if player.collision_rect.collidepoint(tile.rect.bottomright) and tile.collision:
                # Pushing left = go right
                if player.collision_rect.right - tile.rect.right > player.collision_rect.bottom - tile.rect.bottom:
                    player.rect.left = tile.rect.right
                    player.collision_rect.left = tile.rect.right
                # Pushing up = go down
                if player.collision_rect.right - tile.rect.right < player.collision_rect.bottom - tile.rect.bottom:
                    player.rect.top = tile.rect.bottom - PLAYER_SIZE
                    player.collision_rect.top = tile.rect.bottom

        window.blit(player.image, player.rect)

        pygame.display.update()

game_loop()