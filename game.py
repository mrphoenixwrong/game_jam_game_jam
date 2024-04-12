import pygame

pygame.init()

WIDTH, HEIGHT = 1000, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Jam Game")

RUNNING = True

rect = pygame.surface.Surface((50, 50))

while RUNNING:
    window.fill((255,255,255))

    window.blit(rect, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
    pygame.display.update()