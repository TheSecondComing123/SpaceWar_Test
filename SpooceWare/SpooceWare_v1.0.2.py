import pygame
from pygame.locals import *

import random

resize = pygame.transform.scale
load = pygame.image.load
flip_vertical = lambda image: pygame.transform.flip(image, False, True)
rotate = pygame.transform.rotate

pygame.init()


class Ship(pygame.sprite.Sprite):
    def __init__(self, win, x, y, image_filename, *, flip=False):
        super().__init__()

        self.win = win
        self.x = x
        self.y = y

        self.image = pygame.image.load(image_filename)
        if flip:
            self.image = flip_vertical(self.image)

        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self, speed=8, left=False, right=False, up=False, down=False):
        self.win.blit(self.image, self.rect)

        self._move(speed, left, right, up, down)

        if self.x <= 0:
            self.x = 0

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


class Enemy(Ship):
    def __init__(self, win, x, y, image_filename, *, flip=False):
        super().__init__(win, x, y, image_filename, flip=flip)

        self.image = resize(self.image, [s // 2 for s in self.image.get_size()])
        self.rect = self.image.get_rect(center=(self.x, self.y))


class Bullet(pygame.sprite.Sprite):
    def __init__(self, win, x, y, image_filename):
        super().__init__()

        self.win = win
        self.x = x
        self.y = y

        self.image = pygame.image.load(image_filename)

        self.image = rotate(self.image, 90)
        self.image = resize(self.image, [s // 10 for s in self.image.get_size()])

        self.rect = self.image.get_rect(center=(self.x, self.y))

    def update(self, speed=12):
        self.win.blit(self.image, self.rect)

        self.y -= speed
        self.rect.center = (self.x, self.y)


screen = pygame.display.set_mode((1000, 600))

background = resize(load("../space_bg.jpg"), screen.get_size())

player = Ship(screen, *[s // 2 for s in screen.get_size()], "../player_ship.png")

enemy_spawn_event = USEREVENT
enemy_spawn_interval = 1850
pygame.time.set_timer(enemy_spawn_event, enemy_spawn_interval)

bullet_group = pygame.sprite.Group()

enemy_group = pygame.sprite.Group()

running = True
clock = pygame.time.Clock()

while running:
    if pygame.event.get(QUIT):
        running = False
    elif pygame.event.get(enemy_spawn_event):
        enemy_group.add(Enemy(screen,
                              random.randint(50, screen.get_width() - 50),
                              0, "../enemy_ship.png", flip=True))
    elif pygame.event.get(MOUSEBUTTONDOWN):
        bullet_group.add(Bullet(screen, *(player.x, player.y), "../bullet.png"))

    screen.blit(background, (0, 0))

    key = pygame.key.get_pressed()
    player.update(left=key[K_a], right=key[K_d], up=key[K_w], down=key[K_s])

    enemy_group.update(speed=3, down=True)

    for enemy in enemy_group:
        if pygame.sprite.spritecollide(enemy, bullet_group, dokill=True):
            enemy.kill()

    bullet_group.update()

    pygame.display.update()
    clock.tick(60)

pygame.quit()
