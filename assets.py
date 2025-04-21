import pygame

screen=pygame.display.set_mode((900,600))
start_screen=pygame.transform.scale(pygame.image.load("media/start_screen.png"), (900,600))
bgimg=pygame.transform.scale(pygame.image.load("media/background.png"), (900,600))
title=pygame.transform.scale(pygame.image.load("media/title.png"), (341, 183))
left_ss=pygame.transform.scale(pygame.image.load("media/leftslingshot.png"), (80,80))
right_ss=pygame.transform.scale(pygame.image.load("media/rightslingshot.png"), (80,80))
alien=pygame.transform.scale(pygame.image.load("media/alien.png"), (48,48))

block_images = {
    "ice": [pygame.transform.scale(pygame.image.load(f"media/ice_{i}.png"), (48, 48)) for i in range(4)],
    "wood": [pygame.transform.scale(pygame.image.load(f"media/wood_{i}.png"), (48, 48)) for i in range(4)],
    "stone": [pygame.transform.scale(pygame.image.load(f"media/stone_{i}.png"), (48, 48)) for i in range(4)]
}

bird_images = {
    "red": pygame.transform.scale(pygame.image.load("media/Red.png"), (32, 32)),
    "chuck": pygame.transform.scale(pygame.image.load("media/Chuck.png"), (32, 32)),
    "blue": pygame.transform.scale(pygame.image.load("media/Blue.png"), (32, 32)),
    "bomb": pygame.transform.scale(pygame.image.load("media/Bomb.png"), (32, 32))
}