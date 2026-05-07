import pygame
from base_classes import *
from ball_class import *
from constants import *
from wall_class import *
from PyFoot_UI import show_menu
import random
from powerups import *

pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

def draw_boundaries(window):
    block_top_left.draw(window)
    block_bottom_left.draw(window)
    block_top_right.draw(window)
    block_bottom_right.draw(window)
    block_top.draw(window)
    block_bottom.draw(window)

    triangle_top_left.draw(window)
    triangle_bottom_left.draw(window)
    triangle_top_right.draw(window)
    triangle_bottom_right.draw(window)

field = Field()
pygame.display.set_caption("Main Menu")

def run_game(difficulty):
    # Player and ball creation
    player = Player(Vector2(BW + 50, SCREEN_HEIGHT), Vector2(0,0), 100, 175)
    player_score = 0
    ball = Ball(Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2), Vector2(200,-300), 50)
    
    starting_time = pygame.time.get_ticks()
    active_powerups = []
    last_powerup_time = starting_time

    # Bot creation
    if difficulty == "Easy":
            level = EasyBot(Vector2(SCREEN_WIDTH - BW - 150, SCREEN_HEIGHT), Vector2(0,0), 100, 175, player, ball)
    if difficulty == "Medium":
            level = MediumBot(Vector2(SCREEN_WIDTH - BW - 150, SCREEN_HEIGHT), Vector2(0,0), 100, 175, player, ball)
    if difficulty == "Hard":
            level = HardBot(Vector2(SCREEN_WIDTH - BW - 150, SCREEN_HEIGHT), Vector2(0,0), 100, 175, player, ball, starting_time)
    bot_score = 0

    # Game loop       
    run = True
    while run:
        if (pygame.time.get_ticks()- starting_time) < GAME_DURATION:
            dt = clock.tick(60) / 1000

            window.fill((0,0,0))

            # Score display
            font = pygame.font.SysFont(None, 60)
            score_text = font.render(f"{player_score}  -  {bot_score}", True, (255, 0, 0))
            rect = score_text.get_rect(center=(SCREEN_WIDTH / 2, 40))
            window.blit(score_text, rect)

            # Timer display
            time_left = max(0, GAME_DURATION - (pygame.time.get_ticks() - starting_time))
            seconds_left = time_left // 1000
            timer_text = font.render(f"{seconds_left // 60} : {seconds_left % 60:02d}", True, (255, 0, 0))
            timer_rect = timer_text.get_rect(center=(SCREEN_WIDTH / 2, 80))
            window.blit(timer_text, timer_rect)

            level.draw(window)
            level.update(dt, field)
            level._handle_action(dt, field, starting_time)
            
            ball.draw(window)
            ball.update(dt, field, player, level, triangles)
            ball.draw_goal_inscription(window, dt)

            player.draw(window)    
            player.update(dt, field)
            player.collision_player_bot(level)
            player._handle_inputs(dt, field)
            player.bounce_triangle(triangles)

            draw_boundaries(window)

            # Generates power ups at random spots every certain amount of time
            now = pygame.time.get_ticks()
            if now - last_powerup_time > POWERUP_FREQUENCY:
                last_powerup_time = now
                x = random.randint(BW, SCREEN_WIDTH - BW)
                y = random.randint(int(SCREEN_HEIGHT - BH), SCREEN_HEIGHT)
                new_powerup = random.choice([FasterPowerUp, HighJumpPowerUp, LongerBoostPowerUp])
                active_powerups.append(new_powerup(Vector2(x, y), POWERUP_HEIGHT, POWERUP_WIDTH))

            # Makes the powerups stay for a certain duration
            active_powerups = [p for p in active_powerups if pygame.time.get_ticks() - p.spawn_time < POWERUP_DURATION]

            for powerup in active_powerups:
                powerup.draw(window)
                if powerup.check_collected(player) or powerup.check_collected(level):
                    active_powerups.remove(powerup)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            
            who_scored = ball.goal(field)
            if who_scored == "player":
                 player_score += 1
            if who_scored == "bot":
                 bot_score += 1

            pygame.display.flip()
        else:
            return "menu"
    return "quit"


while True:
    difficulty = show_menu()
    result = run_game(difficulty)
    if result == "quit":
        break

pygame.quit()