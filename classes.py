import pygame
import assets

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