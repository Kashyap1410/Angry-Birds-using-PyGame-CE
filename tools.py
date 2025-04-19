import pygame
import random
import assets
import classes

def generate_structure():
    block_types = ["ice"]*5 + ["stone"]*5 + ["wood"]*5 + [None]
    random.shuffle(block_types)
    
    grid = []
    for i in range(4):
        row = []
        for j in range(4):
            b_type = block_types[i*4 + j]
            if b_type:
                row.append(classes.Block(b_type))
            else:
                row.append(None)
        grid.append(row)
    return grid

def draw_structure(grid, start_x, start_y):
    for i in range(4):
        for j in range(4):
            b = grid[i][j]
            if b and b.image:
                assets.screen.blit(b.image, (start_x + j*48, start_y + i*48))

def get_damage(bird_type, block_type):
    damage_map = {
        "red": {"ice": 2, "wood": 2, "stone": 2},
        "chuck": {"ice": 1, "wood": 3, "stone": 1},
        "blue": {"ice": 3, "wood": 1, "stone": 1},
        "bomb": {"ice": 1, "wood": 1, "stone": 3}
    }
    return damage_map[bird_type][block_type]

player1_bird_queue = ["red", "chuck", "blue", "bomb"] * 3
player2_bird_queue = ["red", "chuck", "blue", "bomb"] * 3
random.shuffle(player1_bird_queue)
random.shuffle(player2_bird_queue)

def get_next_bird(player):
    if player == 1:
        return player1_bird_queue.pop(0) if len(player1_bird_queue) > 0 else None
    else:
        return player2_bird_queue.pop(0) if len(player2_bird_queue) > 0 else None

def draw_next_birds(player):
    bird_queue = player1_bird_queue if player == 1 else player2_bird_queue
    for i, bird in enumerate(bird_queue[:2]):
        bird_img = assets.bird_images[bird]
        if player == 1:
            assets.screen.blit(bird_img, (30 + i * 50, 550))
        else:
            bird_img = pygame.transform.flip(bird_img, True, False)
            assets.screen.blit(bird_img, (838 - i * 50, 550))