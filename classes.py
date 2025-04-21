import pygame
import assets
import math
import random

class Bird:
    def __init__(self, bird_type, player):
        self.type = bird_type
        self.player = player
        img = assets.bird_images[bird_type]
        self.image = img if player==1 else pygame.transform.flip(img, True, False)
        self.reset()

    def reset(self):
        if self.player == 1:
            self.x, self.y = 280, 430
        else:
            self.x, self.y = 636, 430
        self.vx = self.vy = 0
        self.path = []
        self.launched = False
        self.step = 0

    def simulate(self, vx, vy, steps=20):
        pts = []
        x, y = self.x, self.y
        for _ in range(steps):
            x += vx
            y += vy
            vy += 1
            if y > 600: break
            pts.append((x, y))
        return pts

    def draw(self):
        assets.screen.blit(self.image, (self.x - self.image.get_width()//2,
                                 self.y - self.image.get_height()//2))

    def update(self):
        if self.launched and self.step < len(self.path):
            self.x, self.y = self.path[self.step]
            self.step += 1

class Block:
    def __init__(self, type):
        self.health = 4
        self.type = type
        self.images = assets.block_images[type]
        self.update_image()

    def update_image(self):
        if self.health > 0:
            self.image = self.images[4 - self.health]
        else:
            self.image = None

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
        self.update_image()

class Alien:
    def __init__(self, start_x, base_y):
        self.start_x = start_x
        self.x = start_x
        self.base_y = base_y
        self.phase = random.uniform(0, 2*math.pi)
        self.image = assets.alien
        self.rect = self.image.get_rect(center=(self.x, self.base_y))
        self.active = True
        self.respawn_timer = 0
        self.respawn_delay = 180

    def update(self):
        if self.active:
            self.x += 2
            self.phase += (2*math.pi) / 100
            self.y = self.base_y + 20*math.sin(self.phase)
            self.rect.center = (self.x, self.y)
            if self.x > 900 + self.image.get_width()/2:
                self.x = -self.image.get_width()/2
        else:
            self.respawn_timer -= 1
            if self.respawn_timer <= 0:
                self.active = True
                self.x = self.start_x
                self.phase = random.uniform(0, 2*math.pi)

    def draw(self):
        assets.screen.blit(self.image, self.rect.topleft)

    def hit(self):
        self.active = False
        self.respawn_timer = self.respawn_delay