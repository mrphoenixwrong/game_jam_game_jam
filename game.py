import pygame, os, json, datetime, random
from pygame.locals import *

from tile import Tile
from player import Player
from lists import *
from npc import NonPlayerCharacter

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
    player = Player((850,450), 0.25, False)
    customers = []

    last_second = int(datetime.datetime.now().strftime("%S"))
    current_milli = 0
    sit_clock = 0
    sit_goal = random.randint(3, 7)

    while RUNNING:
        dt = clock.tick(60)

        world.displayTiles()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False

        key_pressed_is = pygame.key.get_pressed()

        left = False
        right = False
        up = False
        down = False
        if key_pressed_is[K_LEFT] or key_pressed_is[K_a] and not (key_pressed_is[K_RIGHT] or key_pressed_is[K_d]):
            player.rect.x -= player.speed * dt
            player.collision_rect.x -= player.speed * dt
            if player.facing == "right":
                player.turn()
            left = True
        if key_pressed_is[K_RIGHT] or key_pressed_is[K_d] and not (key_pressed_is[K_LEFT] or key_pressed_is[K_a]):
            player.rect.x += player.speed * dt
            player.collision_rect.x += player.speed * dt
            if player.facing == "left":
                player.turn()
            right = True
        if key_pressed_is[K_UP] or key_pressed_is[K_w] and not (key_pressed_is[K_DOWN] or key_pressed_is[K_s]):
            player.rect.y -= player.speed * dt
            player.collision_rect.y -= player.speed * dt
            up = True
        if key_pressed_is[K_DOWN] or key_pressed_is[K_s] and not (key_pressed_is[K_UP] or key_pressed_is[K_w]):
            player.rect.y += player.speed * dt
            player.collision_rect.y += player.speed * dt
            down = True
        if key_pressed_is[K_e]:
            for customer in customers:
                if player.collision_rect.centerx > customer.rect.centerx - TILE_SIZE and player.collision_rect.centerx < customer.rect.centerx + TILE_SIZE:
                    if player.collision_rect.centery > customer.rect.centery - TILE_SIZE and player.collision_rect.centery < customer.rect.centery + TILE_SIZE:
                        if customer.order_status == "ready to order":
                            customer.order_taken()
        
        if left and right:
            if (up and not down) or (down and not up):
                player_moving = True
            else:
                player_moving = False
        elif up and down:
            if (left and not right) or (right and not left):
                player_moving = True
            else:
                player_moving = False
        elif left or right or up or down:
            player_moving = True
        else:
            player_moving = False


        # Collision Detection
        for tile in world.tiles:
            # SIDE COLLISIONS
            # Collide with left side of tile
            if player.collision_rect.collidepoint((tile.rect.left, tile.rect.centery)) and tile.collision:
                player.rect.right = tile.rect.left
                player.collision_rect.right = tile.rect.left
            # Collide with right side of tile
            if player.collision_rect.collidepoint((tile.rect.right, tile.rect.centery)) and tile.collision:
                player.rect.left = tile.rect.right
                player.collision_rect.left = tile.rect.right
            # Collide with top of tile
            if player.rect.collidepoint((tile.rect.centerx, tile.rect.top)) and tile.collision:
                player.rect.bottom = tile.rect.top
                player.collision_rect.bottom = tile.rect.top
            # Collide with bottom of tile
            if player.collision_rect.collidepoint((tile.rect.centerx, tile.rect.bottom)) and tile.collision:
                player.rect.top = tile.rect.bottom - PLAYER_SIZE
                player.collision_rect.top = tile.rect.bottom

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

        current_milli += dt
        if current_milli > 200 and player_moving:
            print(current_milli)
            current_milli = 0
            player.walk()
        elif not player_moving:
            player.walking = False
            player.walk()




        now = int(datetime.datetime.now().strftime("%S"))
        if now > last_second or (now == 0 and last_second == 59):
            last_second = now
            sit_clock += 1
            print(sit_clock)
            for customer in customers:
                if customer.order_status == "ready to order" or customer.order_status == "waiting for food":
                    customer.anger -= 1
                    if customer.anger == 0:
                        customer.karen()
                if customer.order_status == "just sat":
                    customer.wait -= 1
                    if customer.wait == 0:
                        customer.ready_to_order()
                if customer.order_status == "too late!":
                    customer.angered -= 1
                    if customer.angered == 0:
                        customer.stand_up()
                        index = customers.index(customer)
                        customers.pop(index)
            if sit_clock >= sit_goal:
                if len(customers) <= 10:
                    customers.append(NonPlayerCharacter())
                    sit_clock = 0
                    sit_goal = random.randint(3, 7)

        if len(customers) > 0:
            for customer in customers:
                window.blit(customer.image, customer.rect)
        window.blit(player.image, player.rect)

        pygame.display.update()

game_loop()