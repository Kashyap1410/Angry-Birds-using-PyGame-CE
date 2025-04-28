import pygame
import assets, tools
import classes
import game
import math

def quick_game(player1_name, player2_name):
    mode='quick'
    player1_grid = tools.generate_structure()
    player2_grid = tools.generate_structure()

    current_player=1
    player1_score = 0
    player2_score = 0

    current_bird_type = tools.get_next_bird(current_player)
    current_bird = classes.Bird(current_bird_type, current_player)
    dragging = False

    aliens = [
        classes.Alien(start_x=0, base_y=180),
        classes.Alien(start_x=300, base_y=200),
        classes.Alien(start_x=600, base_y=220)
    ]

    game_over = False
    running = True
    clock = pygame.time.Clock()

    running = game.show_info_screen(mode)
    while running and not game_over:
        assets.screen.blit(assets.game_bgimg, (0, 0))
        assets.screen.blit(assets.title, (280, 0))
        assets.screen.blit(assets.left_ss, (250, 420))
        assets.screen.blit(assets.right_ss, (586, 420))

        p1_surf = assets.textbox_font.render(f"{player1_name}: {player1_score}", True, (255,255,255))
        p2_surf = assets.textbox_font.render(f"{player2_name}: {player2_score}", True, (255,255,255))
        assets.screen.blit(p1_surf, (20, 20))
        assets.screen.blit(p2_surf, (880 - p2_surf.get_width(), 20))
        
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
            tools.draw_trajectory(current_bird, current_player)

        if current_bird.launched:
            current_bird.update()

            target_grid = player2_grid if current_bird.player == 1 else player1_grid
            grid_x = 688 if current_bird.player == 1 else 20
            grid_y = 300

            score = tools.check_alien_collisions(current_bird, aliens)
            if current_bird.player == 1:
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
                current_bird = classes.Bird(tools.get_next_bird(current_player), current_player)
        
        if player1_score >= 200 or player2_score >= 200:
            winner = player1_name if player1_score > player2_score else player2_name
            running, mode = game.game_over_screen(winner, 'quick')
            game_over = True

        pygame.display.update()
        clock.tick(60)
    
    return running, mode

def basic_game(player1_name, player2_name):
    mode='basic'
    player1_grid = tools.generate_structure()
    player2_grid = tools.generate_structure()

    current_player=1
    player1_score = 0
    player2_score = 0

    current_bird_type = tools.get_next_bird(current_player)
    current_bird = classes.Bird(current_bird_type, current_player)
    dragging = False

    aliens = [
        classes.Alien(start_x=0, base_y=180),
        classes.Alien(start_x=300, base_y=200),
        classes.Alien(start_x=600, base_y=220)
    ]

    player1_powerups = [classes.Powerup(50, 100, "full_path"), classes.Powerup(120, 100, "double_dmg")]
    player2_powerups = [classes.Powerup(730, 100, "full_path"), classes.Powerup(800, 100, "double_dmg")]

    game_over = False
    running = True
    full_trajectory_enabled = False
    double_damage_enabled = False
    clock = pygame.time.Clock()

    running = game.show_info_screen(mode)
    while running and not game_over:
        assets.screen.blit(assets.game_bgimg, (0, 0))
        assets.screen.blit(assets.title, (280, 0))
        assets.screen.blit(assets.left_ss, (250, 420))
        assets.screen.blit(assets.right_ss, (586, 420))

        p1_surf = assets.textbox_font.render(f"{player1_name}: {player1_score}", True, (255,255,255))
        p2_surf = assets.textbox_font.render(f"{player2_name}: {player2_score}", True, (255,255,255))
        assets.screen.blit(p1_surf, (20, 20))
        assets.screen.blit(p2_surf, (880 - p2_surf.get_width(), 20))

        if current_player == 1:
            for p in player1_powerups:
                p.draw(assets.screen)
        else:
            for p in player2_powerups:
                p.draw(assets.screen)
        
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

                if current_player == 1:
                    for p in player1_powerups:
                        if p.is_clicked(event.pos):
                            if p.type == "full_path":
                                full_trajectory_enabled = True
                            elif p.type == "double_dmg":
                                double_damage_enabled = True
                            p.use()
                else:
                    for p in player2_powerups:
                        if p.is_clicked(event.pos):
                            if p.type == "full_path":
                                full_trajectory_enabled = True
                            elif p.type == "double_dmg":
                                double_damage_enabled = True
                            p.use()

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
            tools.draw_trajectory(current_bird, current_player, full_trajectory_enabled)

        if current_bird.launched:
            current_bird.update()

            target_grid = player2_grid if current_bird.player == 1 else player1_grid
            grid_x = 688 if current_bird.player == 1 else 20
            grid_y = 300

            score = tools.check_alien_collisions(current_bird, aliens)
            if current_bird.player == 1:
                player1_score+=score
            else: 
                player2_score+=score
        
            score = tools.check_block_collisions(current_bird, target_grid, grid_x, grid_y, double_damage_enabled)
            if current_bird.player == 1:
                player1_score += score
            else:
                player2_score += score
            if score!=0:
                current_bird.step = len(current_bird.path)

            if current_bird.step >= len(current_bird.path):
                pygame.time.delay(50)
                current_player = 2 if current_player == 1 else 1
                current_bird = classes.Bird(tools.get_next_bird(current_player), current_player)
                full_trajectory_enabled = False
                double_damage_enabled = False
        
        if tools.structure_demolished(player1_grid):
            running, mode = game.game_over_screen(player1_name, 'basic')
            game_over = True
        if tools.structure_demolished(player2_grid):
            running, mode = game.game_over_screen(player2_name, 'basic')
            game_over = True

        pygame.display.update()
        clock.tick(60)
    
    return running, mode