import pygame
import random, math
import assets
import classes

def generate_structure(): # Create grid structure for both players
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

# 12 birds per player, randomly generated
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
    for i, bird in enumerate(bird_queue[:3]):
        bird_img = assets.bird_images[bird]
        if player == 1:
            assets.screen.blit(bird_img, (30 + i * 50, 550))
        else:
            bird_img = pygame.transform.flip(bird_img, True, False)
            assets.screen.blit(bird_img, (838 - i * 50, 550))

def draw_trajectory(current_bird, current_player):
    mx, my = pygame.mouse.get_pos()
    start_x, start_y = (280, 430) if current_player == 1 else (636, 430)
    dx = mx - start_x
    dy = my - start_y
    distance = math.hypot(dx, dy)
    max_distance = 150
    if distance > max_distance:
        scale = max_distance / distance
        dx *= scale
        dy *= scale
    vx = -dx * 0.2
    vy = -dy * 0.2
    trajectory = current_bird.simulate(vx, vy, steps=15)
       
    pygame.draw.line(assets.screen, (255, 255, 255), (start_x, start_y), (start_x+dx, start_y+dy), 2)
    for i, point in enumerate(trajectory):
        pygame.draw.circle(assets.screen, (255, 255, 255, max((255-30*i),0)), (int(point[0]), int(point[1])), (4-i//6))

def check_alien_collisions(bird, aliens):
    bird_rect = pygame.Rect(bird.x - 16, bird.y - 16, 32, 32)
    for alien in aliens:
        alien_rect = pygame.Rect(alien.x - 24, alien.y - 24, 48, 48)
        if alien.active and bird_rect.colliderect(alien_rect):
            alien.hit()
            return 5 # Score of 5 on hitting an alien
    return 0

def check_block_collisions(bird, grid, grid_x, grid_y):
    bird_rect = pygame.Rect(bird.x - 16, bird.y - 16, 32, 32)
    for i in range(4):
        for j in range(4):
            block = grid[i][j]
            if block and block.health > 0:
                block_rect = pygame.Rect(grid_x + j*48, grid_y + i*48, 48, 48)
                if bird_rect.colliderect(block_rect):
                    damage = get_damage(bird.type, block.type)
                    block.take_damage(damage)
                    return damage * 10 # Return score
    return 0