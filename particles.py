import pygame
from random import randint

class Particle(pygame.sprite.Sprite):
    def __init__(self, direction, speed, pos, group):
        super().__init__(group)
        self.direction = direction
        self.speed = speed
        self.pos = pos

        self.alpha = 255
        self.fade_speed = 200

        self.group = group
        self.create_surf()


    def create_surf(self):
        self.image = pygame.image.load("images/misc/snowflake.png")
        self.rect = self.image.get_rect(center=self.pos)

    def move(self, dt):
        self.pos += self.direction * self.speed * dt
        self.rect.center = self.pos

    def update(self, dt):
        self.move(dt)
        self.fade(dt)

    def fade(self, dt):
        self.alpha -= self.fade_speed * dt
        self.image.set_alpha(self.alpha)
        if self.alpha < 1:
            self.kill()


class Sparkle(Particle):
    def __init__(self, direction, speed, pos, group):
        super.__init__(direction, speed, pos, group)
