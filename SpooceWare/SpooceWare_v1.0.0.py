import pygame
from pygame.locals import *

resize = pygame.transform.scale
load = pygame.image.load

pygame.init()


class Ship(pygame.sprite.Sprite):
    def __init__(self, win, x, y):
        super().__init__()

        self.win = win
        self.x = x
        self.y = y

        self.image = pygame.image.load("../player_ship.png")
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self, speed=8, left=False, right=False, up=False, down=False):
        self.win.blit(self.image, self.rect)

        self._move(speed, left, right, up, down)
        self.rect.center = (self.x, self.y)

    def _move(self, speed, left=False, right=False, up=False, down=False):
        if left:
            self.x -= speed
        elif right:
            self.x += speed
        elif up:
            self.y -= speed
        elif down:
            self.y += speed


screen = pygame.display.set_mode((1000, 600))

background = resize(load("../space_bg.jpg"), screen.get_size())

player = Ship(screen, *[s // 2 for s in screen.get_size()])

running = True
clock = pygame.time.Clock()

while running:
    if pygame.event.get(QUIT):
        running = False

    screen.blit(background, (0, 0))

    key = pygame.key.get_pressed()
    player.update(left=key[K_a], right=key[K_d], up=key[K_w], down=key[K_s])

    pygame.display.update()
    clock.tick(60)

pygame.quit()
