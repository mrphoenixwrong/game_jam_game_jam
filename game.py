import pygame, os, json

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

class Tile:
    def __init__(self, image, rect, collision):
        self.image = image
        self.rect = rect
        self.collision = collision


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

while RUNNING:
    window.fill((255,255,255))

    window.blit(rect, (0,0))
    world.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
    pygame.display.update()