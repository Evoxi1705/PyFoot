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

class TempField:
    def get_top(self): return 0
    def get_bottom(self): return SCREEN_HEIGHT
    def get_left(self): return 0 + BW
    def get_right(self): return SCREEN_WIDTH - BW

field = TempField()
pygame.display.set_caption("Main Menu")

def run_game(difficulty):
    # Player and ball creation
    player = Player(Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT), Vector2(0,0), 50, 100)
    player_score = 0
    ball = Ball(Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2), Vector2(200,-300), 30)
    
    starting_time = pygame.time.get_ticks()
    active_powerups = []
    last_powerup_time = starting_time

    # Bot creation
    if difficulty == "Easy":
            level = EasyBot(Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT), Vector2(0,0), 50, 100, player, ball)
    if difficulty == "Medium":
            level = MediumBot(Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT), Vector2(0,0), 50, 100, player, ball)
    if difficulty == "Hard":
            level = HardBot(Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT), Vector2(0,0), 50, 100, player, ball, starting_time)
    bot_score = 0

    # Game loop       
    run = True
    while run:
        if (pygame.time.get_ticks()- starting_time) < GAME_DURATION:
            dt = clock.tick(60) / 1000  # dt is roughly 0.016 at 60fps
            
            window.fill((0,0,0))

            # Score display
            font = pygame.font.SysFont(None, 60)
            score_text = font.render(f"{player_score}  -  {bot_score}", True, (255, 0, 0))
            rect = score_text.get_rect(center=(SCREEN_WIDTH / 2, 40))
            window.blit(score_text, rect)

            # Timer display
            time_left = max(0, GAME_DURATION - (pygame.time.get_ticks() - starting_time)) # max to prevent it going negative in the last frame
            seconds_left = time_left // 1000
            timer_text = font.render(f"{seconds_left // 60} : {seconds_left % 60:02d}", True, (255, 0, 0)) #02d makes it two digits
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
            player._handle_inputs(dt, field)
            player.bounce_triangle(triangles)

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

            # Generates power ups at random spots every certain amount of time
            now = pygame.time.get_ticks()
            if now - last_powerup_time > POWERUP_FREQUENCY:
                last_powerup_time = now
                x = random.randint(field.get_left(), field.get_right())
                y = random.randint(field.get_top(), field.get_bottom())
                new_powerup = random.choice([FasterPowerUp, HighJumpPowerUp, LongerBoostPowerUp])
                active_powerups.append(new_powerup(Vector2(x, y), POWERUP_HEIGHT, POWERUP_WIDTH))

            # Makes the powerups stay for a certain duration
            active_powerups = [p for p in active_powerups if pygame.time.get_ticks() - p.spawn_time < POWERUP_DURATION]

            for powerup in active_powerups:
                powerup.draw(window)


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