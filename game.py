import pygame, os, json, datetime, random
from pygame.locals import *

from tile import Tile
from player import Player
from lists import *
from npc import NonPlayerCharacter

from chef import Chef
from random import randint, choice, uniform

from particles import Particle

pygame.init()


particle_group = pygame.sprite.Group()

floating_particle_timer = pygame.event.custom_type()
pygame.time.set_timer(floating_particle_timer, 10)

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

def title_loop():
    title_screen = pygame.image.load(os.path.join("images\\screens", "WSCtitlemenu.png"))


    start_button = pygame.font.Font('fonts\\DePixelHalbfett.ttf', 20).render(f"START JOB", True, (255, 255, 255))
    start_rect = start_button.get_rect(center=((950-560)/2 + 560, (478-434)/2 + 434))

    controls_button = pygame.font.Font('fonts\\DePixelHalbfett.ttf', 20).render(f"CONTROLS", True, (255, 255, 255))
    controls_rect = controls_button.get_rect(center=((950-560)/2 + 560, (528-486)/2 + 486))

    credits_button = pygame.font.Font('fonts\\DePixelHalbfett.ttf', 20).render(f"CREDITS", True, (255, 255, 255))
    credits_rect = credits_button.get_rect(center=((950-560)/2 + 560, (584-536)/2 + 536))

    pygame.mixer.music.load(os.path.join('music', 'Chilly Menu - Worst Served Cold OST(1).mp3'))
    pygame.mixer.music.play(-1)

    RUNNING = True
    while RUNNING:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
                CONTINUE = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if 560 <= mouse[0] <= 950 and 434 <= mouse[1] <= 478:
                    return True
                if 560 <= mouse[0] <= 950 and 486 <= mouse[1] <= 528:
                    RUNNING, CONTINUE = transition_loop(False, "controls", 0, 0)
                if 560 <= mouse[0] <= 950 and 536 <= mouse[1] <= 584:
                    RUNNING, CONTINUE = transition_loop(False, "credits", 0, 0)

        window.blit(title_screen, (0,0))
        window.blit(start_button, start_rect)
        window.blit(controls_button, controls_rect)
        window.blit(credits_button, credits_rect)

        pygame.display.update()
    return CONTINUE

def game_loop(day, time_left, rate, max_customers, customer_goal, can_cold):
    world, RUNNING = createWorld()
    CONTINUE = True
    player = Player((850,450), 0.25, False)
    chef = Chef((850,200))
    
    customers = []
    food_to_prepare = []
    prepared_food = []

    last_second = int(datetime.datetime.now().strftime("%S"))
    current_milli = 0
    sit_clock = 0
    sit_goal = random.randint(rate[0], rate[1])

    happiness = 0

    e_released = True
    pygame.mixer.music.load(os.path.join('music', 'Chilly Menu - Worst Served Cold OST(1).mp3'))
    pygame.mixer.music.play(-1)
    while RUNNING:
        dt = clock.tick(60)

        world.displayTiles()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
                CONTINUE = False

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
            if e_released:
                e_released = False
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
                                    player.set_bar()
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
                        player.set_bar()
        else:
            e_released = True

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
            if player.collision_rect.collidepoint((customer.rect.left, tile.rect.centery)):
                player.rect.right = tile.rect.left
                player.collision_rect.right = tile.rect.left
            if player.collision_rect.collidepoint((customer.rect.left, tile.rect.centery)):
                player.rect.left = tile.rect.right
                player.collision_rect.left = tile.rect.right
            if player.collision_rect.collidepoint((customer.rect.left, tile.rect.centery)):
                player.rect.bottom = tile.rect.top
                player.collision_rect.bottom = tile.rect.top
            if player.collision_rect.collidepoint((customer.rect.left, tile.rect.centery)):
                player.rect.top = tile.rect.bottom - PLAYER_SIZE
                player.collision_rect.top = tile.rect.bottom


        #chef border collision (so they don't go into the void)
        #left walll
        if chef.rect.left < 750:
            chef.rect.left = 750
            chef.direction = "right"
        #right wall
        if chef.rect.right > 900:
            chef.rect.right = 900
            chef.direction = "none"

        player.place_bar()
        
        #snowflakes!
        def spawn_floating_particles():
            pos = player.collision_rect.x + randint(-1,30), player.collision_rect.y + randint(-20,20)
            snow_direct = pygame.math.Vector2(0,-1)
            speed = randint(1,24)
            Particle(snow_direct, speed, pos, particle_group)
            particle_group.draw(window)

        if event.type == floating_particle_timer:
            spawn_floating_particles()
        
        particle_group.update(dt/1000)


        now = int(datetime.datetime.now().strftime("%S"))
        if now > last_second or (now == 0 and last_second == 59):
            last_second = now
            sit_clock += 1
            time_left -= 1
            if time_left == 0:
                RUNNING = False
                CONTINUE = True

            if player.has_plate:
                if player.freeze_timer > 0:
                        player.freeze_timer -= 1
                        player.set_bar()
                if player.freeze_timer == 0:
                    held_food[0] = held_food[0].replace("hot", "cold")
                    held_food[1] = pygame.image.load(os.path.join('images\\food', f'{held_food[0]}.png'))
            if len(food_to_prepare) < 4 and len(food_to_prepare) > 0:
                food_to_prepare[0].prepare_time -= 1
                if food_to_prepare[0].prepare_time == 1:
                    chef.direction = "left"
                if food_to_prepare[0].prepare_time == 0 and len(prepared_food) < 4:
                    food_item = food_to_prepare[0]
                    food_to_prepare.pop(0)

                    coordinates = choice(FOOD_SPAWNS)
                    index = FOOD_SPAWNS.index(coordinates)
                    FOOD_SPAWNS.pop(index)
                    food_item.cook_dish(coordinates)
                    prepared_food.append([f"{food_item.type}_hot", food_item.hot_image, food_item.hot_rect])

            for customer in customers:
                if customer.order_status == "just sat":
                    customer.wait -= 1
                    if customer.wait == 0:
                        customer.ready_to_order(can_cold)
                if customer.order_status == "ready to order":
                    customer.more_angry()
                    if customer.anger == 0:
                        customer.karen()
                if customer.order_status == "waiting for food":
                    customer.more_angry()
                    if customer.anger == 0:
                        customer.karen()
                if customer.order_status == "food prepared":
                    customer.more_angry()
                    if customer.anger == 0:
                        customer.karen()
                        print("mad and should leave")
                if customer.order_status == "too late!" or customer.order_status == "order complete":
                    if customer.leaving == 0:
                        customer.stand_up()
                        index = customers.index(customer)
                        customers.pop(index)
                        
                        if customer.order_status == "order complete":
                            happiness += 1
                    customer.leaving -= 1
            if sit_clock >= sit_goal:
                if len(customers) <= max_customers:
                    customers.append(NonPlayerCharacter(player))
                    sit_clock = 0
                    sit_goal = random.randint(rate[0], rate[1])
            
        chef.move(dt)


        current_milli += dt
        if current_milli > 200:
            chef.switch_image()
            current_milli = 0
            if player_moving:
                player.walk()
            else:
                player.walking = False
                player.walk()

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
            window.blit(player.bar, player.bar_rect)


        
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

    pygame.mixer.music.stop()
    if CONTINUE:
        return transition_loop(True, False, happiness, customer_goal)
    return False, False


def transition_loop(happiness_matters, purpose, happiness, customer_goal):
    
    if happiness_matters:
        if happiness >= customer_goal:
            pygame.mixer.music.load(os.path.join('music', 'win.mp3'))
            pygame.mixer.music.play(1)
            screen_card = pygame.image.load(os.path.join("images\\screens", "WSCdaycomplete.png"))
            RESTART = False
        else:
            pygame.mixer.music.load(os.path.join('music', 'wompwomp.mp3'))
            pygame.mixer.music.play(1)
            screen_card = pygame.image.load(os.path.join("images\\screens", "WSCfired.png"))
            RESTART = True
    else:
        screen_card = pygame.image.load(os.path.join("images\\screens", f"{purpose}.png"))
        if purpose == "WSCpromoted":
            pygame.mixer.music.load(os.path.join('music', 'win.mp3'))
            pygame.mixer.music.play(1)

    RUNNING = True
    while RUNNING:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
                RESTART = False
                CONTINUE = False
        key_pressed_is = pygame.key.get_pressed()
        if key_pressed_is[K_RETURN]:
            RUNNING = False
            CONTINUE = True
        window.blit(screen_card, (0,0))

        pygame.display.update()

    RUNNING = True
    while RUNNING:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUNNING = False
                RESTART = False
                CONTINUE = False
        key_pressed_is = pygame.key.get_pressed()
        if not key_pressed_is[K_RETURN]:
            RUNNING = False
            CONTINUE = True
        window.blit(screen_card, (0,0))

        pygame.display.update()
    if happiness_matters:
        return CONTINUE, RESTART
    else:
        print(CONTINUE)
        return CONTINUE, CONTINUE