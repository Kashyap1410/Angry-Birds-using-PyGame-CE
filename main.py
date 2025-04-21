import pygame
pygame.init()
pygame.display.set_caption("FeatherFall: Siege of Avaria!")

import math
import assets, tools
import classes

player1_grid = tools.generate_structure()
player2_grid = tools.generate_structure()

current_player=1
player1_score = 0
player2_score = 0
font = pygame.font.SysFont(None, 36)
player1_name = player2_name = None

current_bird_type = tools.get_next_bird(current_player)
current_bird = classes.Bird(current_bird_type, current_player)
dragging = False
trajectory=[]

aliens = [
    classes.Alien(start_x=0, base_y=200),
    classes.Alien(start_x=450, base_y=200)
]

# Main loop
clock = pygame.time.Clock()
running = True
started = False
while running:
    if not started:
        running, started = tools.show_start_screen()
        if not running: break
    
    if player1_name is None:
        running, player1_name = tools.take_name_input()
        if not running: break
    if player2_name is None:
        running, player2_name = tools.take_name_input()
        if not running: break

    assets.screen.blit(assets.bgimg, (0, 0))
    assets.screen.blit(assets.title, (280, 0))
    assets.screen.blit(assets.left_ss, (250, 420))
    assets.screen.blit(assets.right_ss, (586, 420))

    p1_surf = font.render(f"{player1_name}: {player1_score}", True, (255,255,255))
    p2_surf = font.render(f"{player2_name}: {player2_score}", True, (255,255,255))
    assets.screen.blit(p1_surf, (20, 20))
    assets.screen.blit(p2_surf, (900 - p2_surf.get_width() - 20, 20))
    
    tools.draw_structure(player1_grid, 20, 300)
    tools.draw_structure(player2_grid, 688, 300)
    tools.draw_next_birds(1)
    tools.draw_next_birds(2)
    current_bird.draw()
    for a in aliens:
        a.update()
        if a.active: a.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if abs(mx - current_bird.x) < 20 and abs(my - current_bird.y) < 20:
                dragging = True

        elif event.type == pygame.MOUSEBUTTONUP and dragging:
            dragging = False
            mx,my = pygame.mouse.get_pos()
            dx, dy = mx - current_bird.x, my - current_bird.y
            distance = math.hypot(dx, dy)
            max_distance = 150
            if distance > max_distance:
                scale = max_distance / distance
                dx *= scale
                dy *= scale
            vx_launch = -dx * 0.2
            vy_launch = -dy * 0.2
            current_bird.path = current_bird.simulate(vx_launch, vy_launch, steps=200)
            current_bird.vx, current_bird.vy = vx_launch, vy_launch
            current_bird.launched = True
            current_bird.step = 0

    if dragging:
        mx, my = pygame.mouse.get_pos()
        start_x, start_y = (280, 430) if current_player == 1 else (636, 430)
        dx = mx - start_x
        dy = my - start_y
        power = min(math.hypot(dx, dy), 150) / 5
        angle = (math.atan2(dy, dx) + math.pi) % (2 * math.pi)
        vx = -dx * 0.2
        vy = -dy * 0.2
        trajectory = current_bird.simulate(vx, vy, steps=20)
        pygame.draw.line(assets.screen, (255, 255, 255), (start_x, start_y), (mx, my), 2)

    if dragging:
        for i, point in enumerate(trajectory):
            pygame.draw.circle(assets.screen, (255, 255, 255, max((255-15*i),0)), (int(point[0]), int(point[1])), (4-i//6))

    if current_bird.launched:
        current_bird.update()

        target_grid = player2_grid if current_bird.player == 1 else player1_grid
        grid_x = 688 if current_bird.player == 1 else 20
        grid_y = 300

        score = tools.check_alien_collisions(current_bird, aliens)
        if current_bird.player==1:
            player1_score+=score
        else: 
            player2_score+=score
       
        score = tools.check_block_collisions(current_bird, target_grid, grid_x, grid_y)
        if current_bird.player == 1:
            player1_score += score
        else:
            player2_score += score
        if score!=0:
            current_bird.step = len(current_bird.path)

        if current_bird.step >= len(current_bird.path):
            pygame.time.delay(50)
            current_player = 2 if current_player == 1 else 1
            next_bird_type = tools.get_next_bird(current_player)
            if next_bird_type:
                current_bird = classes.Bird(next_bird_type, current_player)
            else:
                print("No birds left. Game over!")
                running = False

    current_bird.draw()

    pygame.display.update()
    clock.tick(60)