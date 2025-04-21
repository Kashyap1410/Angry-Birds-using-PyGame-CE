import pygame
import random
import assets
import classes

def show_start_screen():
    running = True
    started = False
    clock = pygame.time.Clock()
    while not started and running:
        assets.screen.blit(assets.start_screen, (0,0))
        start_button=pygame.Rect(340, 490, 210, 60)
        pygame.draw.rect(assets.screen, (255,0,0), start_button, 2)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(pygame.mouse.get_pos()):
                    print("pakad liya")
                    return True, True
        pygame.display.update()
        clock.tick(60)
    return False, False

def take_name_input():
    running = True
    done = False
    name = ""
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if name.strip():
                        done = True
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode
        
        assets.screen.fill((0,0,0))
        txt = font.render("Enter Name: " + name, True, (255, 255, 255))
        assets.screen.blit(txt, (450-txt.get_width()//2, 300-txt.get_height()//2))

        pygame.display.update()
        clock.tick(60)
    return running, name.strip()

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
    for i, bird in enumerate(bird_queue[:3]):
        bird_img = assets.bird_images[bird]
        if player == 1:
            assets.screen.blit(bird_img, (30 + i * 50, 550))
        else:
            bird_img = pygame.transform.flip(bird_img, True, False)
            assets.screen.blit(bird_img, (838 - i * 50, 550))

def check_alien_collisions(bird, aliens):
    bird_rect = pygame.Rect(bird.x - 16, bird.y - 16, 32, 32)
    for alien in aliens:
        if alien.active and bird_rect.colliderect(alien.rect):
            alien.hit()
            return 5
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
                    return damage * 10
    return 0