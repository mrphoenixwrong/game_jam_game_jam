
import pygame, os, json
from pygame.locals import *

from tile import Tile
from player import Player

from chef import Chef
from random import randint, choice

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
                    tile = Tile(tile, (current_col * TILE_SIZE, current_row * TILE_SIZE), False)
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
    player = Player((0,0), False)
    chef = Chef((750,200))
    direction = choice(["left", "right"])
    chef_move_count = 0
    

    while RUNNING:
        dt = clock.tick(60)

        world.displayTiles()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False

        key_pressed_is = pygame.key.get_pressed()
        
        if key_pressed_is[K_LEFT] or key_pressed_is[K_a]:
            player.rect.x -= 0.3 * dt
            player.collision_left(chef, 0.3*dt)
        if key_pressed_is[K_RIGHT] or key_pressed_is[K_d]:
            player.rect.x += 0.3 * dt
            player.collision_right(chef, 0.3*dt)
        if key_pressed_is[K_UP] or key_pressed_is[K_w]:
            player.rect.y -= 0.3 * dt
            player.collision_up(chef, 0.3*dt)
        if key_pressed_is[K_DOWN] or key_pressed_is[K_s]:
            player.rect.y += 0.3 * dt
            player.collision_down(chef, 0.3*dt)

        if player.rect.x < TILE_SIZE:
            player.rect.x = TILE_SIZE
        if player.rect.x > WIDTH - 2 * TILE_SIZE:
            player.rect.x = WIDTH - 2 * TILE_SIZE
        if player.rect.y < 2 * TILE_SIZE:
            player.rect.y = 2 * TILE_SIZE
        if player.rect.y > HEIGHT - 2 * TILE_SIZE:
            player.rect.y = HEIGHT - 2 * TILE_SIZE

        
        #chef border collision (so they don't go into the void)
        #left walll
        if chef.rect.x < 751:
            chef.rect.x = 750
        #right wall
        if chef.rect.x > 870:
            chef.rect.x = 870       
        
        chance = randint(1,100)
        if chance == 24:
            if chef_move_count >= 10:
                direction = choice(["left", "right"])
                chef_move_count = 0
            chef.cookin(direction)
            chef_move_count += 1
            

        window.blit(player.image, player.rect)
        window.blit(chef.image, chef.rect)
        

        pygame.display.update()

game_loop()
