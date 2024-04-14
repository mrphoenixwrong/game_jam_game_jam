import pygame, os, json, datetime, random
from pygame.locals import *

from tile import Tile
from player import Player
from lists import *
from npc import NonPlayerCharacter

from chef import Chef
from random import randint, choice

pygame.init()

WIDTH, HEIGHT = 1000, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Jam Game")

TILE_SIZE = 50
PLAYER_SIZE = 40

font = pygame.font.Font('fonts\\DePixelHalbfett.ttf', 25)

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


def game_loop(day, time_left, rate, max_customers, customer_goal, can_cold):
    world, RUNNING = createWorld()
    GO_TO_ENDING = True
    player = Player((850,450), 0.25, False)
    chef = Chef((750,200))
    direction = choice(["left", "right"])
    chef_move_count = 0
    
    customers = []
    food_to_prepare = []
    prepared_food = []

    last_second = int(datetime.datetime.now().strftime("%S"))
    current_milli = 0
    sit_clock = 0
    sit_goal = random.randint(rate[0], rate[1])

    happiness = 0

    while RUNNING:
        dt = clock.tick(60)

        world.displayTiles()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
                GO_TO_ENDING = False

        key_pressed_is = pygame.key.get_pressed()

        left = False
        right = False
        up = False
        down = False
        if key_pressed_is[K_LEFT] or key_pressed_is[K_a] and not (key_pressed_is[K_RIGHT] or key_pressed_is[K_d]):
            player.rect.x -= player.speed * dt
            player.collision_rect.x -= player.speed * dt
            player.collision_left(chef, player.speed * dt)
            if len(customers) > 0:
                for i in range(0,len(customers)):
                    player.collision_left(customers[i], player.speed * dt)
            if player.facing == "right":
                player.turn()
            left = True

        if key_pressed_is[K_RIGHT] or key_pressed_is[K_d] and not (key_pressed_is[K_LEFT] or key_pressed_is[K_a]):
            player.rect.x += player.speed * dt
            player.collision_rect.x += player.speed * dt
            player.collision_right(chef, player.speed * dt)
            if len(customers) > 0:
                for i in range(0,len(customers)):
                    player.collision_right(customers[i], player.speed * dt)
            if player.facing == "left":
                player.turn()
            right = True

        if key_pressed_is[K_UP] or key_pressed_is[K_w] and not (key_pressed_is[K_DOWN] or key_pressed_is[K_s]):
            player.rect.y -= player.speed * dt
            player.collision_rect.y -= player.speed * dt
            player.collision_up(chef, player.speed * dt)
            if len(customers) > 0:
                for i in range(0,len(customers)):
                    player.collision_up(customers[i], player.speed * dt)
            up = True

        if key_pressed_is[K_DOWN] or key_pressed_is[K_s] and not (key_pressed_is[K_UP] or key_pressed_is[K_w]):
            player.rect.y += player.speed * dt
            player.collision_rect.y += player.speed * dt
            player.collision_down(chef, player.speed * dt)
            if len(customers) > 0:
                for i in range(0,len(customers)):
                    player.collision_down(customers[i], player.speed * dt)
            down = True

        if key_pressed_is[K_e]:
            for customer in customers:
                if player.collision_rect.centerx > customer.rect.centerx - TILE_SIZE and player.collision_rect.centerx < customer.rect.centerx + TILE_SIZE:
                    if player.collision_rect.centery > customer.rect.centery - TILE_SIZE and player.collision_rect.centery < customer.rect.centery + TILE_SIZE + 20:
                        if customer.order_status == "ready to order":
                            customer.order_taken()
                            food_to_prepare.append(customer.order)
                            customer.set_bar()
                        elif customer.order_status == "waiting for food" and player.has_plate:
                            if held_food[0] == customer.order.full_order:
                                held_food = []
                                player.has_plate = False
                                customer.received_order()
            if not player.has_plate and len(prepared_food) > 0:
                if player.collision_rect.centerx > prepared_food[0][2].centerx - TILE_SIZE and player.collision_rect.centerx < prepared_food[0][2].centerx + TILE_SIZE:
                    held_food = prepared_food[0]
                    prepared_food.pop(0)
                    player.pick_up()
                    FOOD_SPAWNS.append(held_food[2].topleft)
            elif player.has_plate:
                if player.collision_rect.centerx > 850 and player.collision_rect.centery > 450:
                    held_food = []
                    player.has_plate = False

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

        if player.has_plate:
            if player.facing == "left":
                held_food[1] = pygame.transform.flip(pygame.image.load(os.path.join('images\\food', f'{held_food[0]}.png')), True, False)
                held_food[2].centerx = player.rect.centerx + 15
            
            elif player.facing == "right":
                held_food[1] = pygame.transform.flip(pygame.image.load(os.path.join('images\\food', f'{held_food[0]}.png')), True, False)
                held_food[2].centerx = player.rect.centerx - 15
            held_food[2].y = player.rect.top + 12


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

        for customer in customers:
            pass

        #chef border collision (so they don't go into the void)
        #left walll
        if chef.rect.x < 751:
            chef.rect.x = 750
        #right wall
        if chef.rect.x > 870:
            chef.rect.x = 870
        
        #chef idle movement
        chance = randint(1,100)
        if chance == 23:
            if chef_move_count >= 10:
                direction = choice(["left", "right"])
                chef_move_count = 0
            chef.cookin(direction)
            chef_move_count += 1

        current_milli += dt
        if current_milli > 200 and player_moving:
            current_milli = 0
            player.walk()
        elif not player_moving:
            player.walking = False
            player.walk()

        now = int(datetime.datetime.now().strftime("%S"))
        if now > last_second or (now == 0 and last_second == 59):
            last_second = now
            sit_clock += 1
            time_left -= 1
            if time_left == 0:
                RUNNING = False

            if player.has_plate:
                if player.freeze_timer == 0:
                    held_food[0] = held_food[0].replace("hot", "cold")
                    held_food[1] = pygame.image.load(os.path.join('images\\food', f'{held_food[0]}.png'))
                player.freeze_timer -= 1
            if len(food_to_prepare) < 4 and len(food_to_prepare) > 0:
                food_to_prepare[0].prepare_time -= 1
                if food_to_prepare[0].prepare_time == 0:
                    food_item = food_to_prepare[0]
                    food_to_prepare.pop(0)

                    coordinates = choice(FOOD_SPAWNS)
                    index = FOOD_SPAWNS.index(coordinates)
                    FOOD_SPAWNS.pop(index)
                    food_item.cook_dish(coordinates)
                    prepared_food.append([f"{food_item.type}_hot", food_item.hot_image, food_item.hot_rect])

            for customer in customers:
                if customer.order_status == "just sat":
                    if customer.wait == 0:
                        customer.ready_to_order(can_cold)
                    customer.wait -= 1
                if customer.order_status == "ready to order":
                    if customer.anger == 0:
                        customer.karen()
                    customer.more_angry()
                if customer.order_status == "waiting for food":
                    if customer.anger == 0:
                        customer.karen()
                    customer.more_angry()
                if customer.order_status == "food prepared":
                    if customer.anger == 0:
                        customer.karen()
                        print("mad and should leave")
                    customer.more_angry()
                if customer.order_status == "too late!" or customer.order_status == "order complete":
                    if customer.leaving == 0:
                        customer.stand_up()
                        index = customers.index(customer)
                        customers.pop(index)
                        
                        if customer.order_status == "too late!":
                            happiness -= 1
                        else:
                            happiness += 1
                    customer.leaving -= 1
            if sit_clock >= sit_goal:
                if len(customers) <= max_customers:
                    customers.append(NonPlayerCharacter(player))
                    sit_clock = 0
                    sit_goal = random.randint(rate[0], rate[1])

        for customer in customers:
            if customer.rect.y <= player.rect.y:
                window.blit(customer.image, customer.rect)
        window.blit(player.image, player.rect)
        if player.has_plate:
            window.blit(held_food[1], held_food[2])
        for food in prepared_food:
            window.blit(food[1], food[2])
        window.blit(chef.image, chef.rect)

        for customer in customers:
            if customer.rect.y > player.rect.y:
                window.blit(customer.image, customer.rect)
        for customer in customers:
            if customer.order_status == "ready to order" or customer.order_status == "waiting for food" or customer.order_status == "food prepared":
                window.blit(customer.thought_image, customer.thought_rect)
                if customer.order_status == "waiting for food" or customer.order_status == "food prepared":
                    window.blit(customer.food_image, customer.food_rect)
            window.blit(customer.bar, customer.bar_rect)


        
        day_text = font.render(f"DAY {day}", True, (0, 0, 0))
        timer = font.render(f"{time_left//60}:{f'{time_left % 60:02}'}", True, (0, 0, 0))
        happiness_meter = font.render(f"{happiness}/{customer_goal}", True, (0, 0, 0))
        happiness_rect = happiness_meter.get_rect()
        happiness_rect.centerx = 500
        happiness_rect.top = 10

        window.blit(day_text, (15, 10))
        window.blit(timer, (920, 10))
        window.blit(happiness_meter, happiness_rect)

        pygame.display.update()

    
    return GO_TO_ENDING