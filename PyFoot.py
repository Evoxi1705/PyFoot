import pygame
import random
from base_classes import *
from ball_class import *
from constants import *
from wall_class import *
from PyFoot_UI import show_menu
from powerups import *

"""
This file is the main game loop. It's where all the dots finally connect!
Running this file will let you play our game,
Have fun!
"""

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("Formula 1 Theme [_QmiNC9d788].mp3")
pygame.mixer.music.play(-1) 
pygame.display.set_caption("Main Menu")
clock = pygame.time.Clock()
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
field = Field()
background = pygame.transform.scale(pygame.image.load("grafiti.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
def draw_boundaries(window):
    """
    Draws the boundaries of the field on the screen.
    
    Args:
        window (pygame display): Canvas on which the boundaries have to be drawn.
    """
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


# Main function   
def run_game(difficulty):
    """
    Runs the main game loop.
    
    Args:
        difficulty (string): String indicating the chosen difficulty.
    """
    # Player and ball creation
    player = Player(Vector2(BW + TH, SCREEN_HEIGHT), Vector2(0,0), 100, 190)
    player_score = 0
    ball = Ball(Vector2(SCREEN_WIDTH/2, SCREEN_HEIGHT/2), Vector2(200,-300), 50)
    
    starting_time = pygame.time.get_ticks()
    active_powerups = []
    last_powerup_time = starting_time

    # Bot creation
    if difficulty == "Easy":
            level = EasyBot(Vector2(SCREEN_WIDTH - BW - TH - 100, SCREEN_HEIGHT), Vector2(0,0), 100, 190, player, ball)
    if difficulty == "Medium":
            level = MediumBot(Vector2(SCREEN_WIDTH - BW - TH - 100 , SCREEN_HEIGHT), Vector2(0,0), 100, 190, player, ball)
    if difficulty == "Hard":
            level = HardBot(Vector2(SCREEN_WIDTH - BW - TH - 100, SCREEN_HEIGHT), Vector2(0,0), 100, 190, player, ball, starting_time)
    bot_score = 0

    # Game loop       
    run = True
    while run:
        if (pygame.time.get_ticks()- starting_time) < GAME_DURATION:
            dt = clock.tick(60) / 1000  # dt is roughly 0.016 at 60fps
            
            window.blit(background, (0, 0))

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
            level._handle_action(dt, field, starting_time, active_powerups)
            
            # Ball rendering
            ball.draw(window)
            ball.update(dt, field, player, level, triangles)
            ball.draw_goal_inscription(window, dt)

            # Player rendering
            player.draw(window)    
            player.update(dt, field)
            player._handle_inputs(dt, field)
            player.bounce_triangle(triangles)

            # Arena rendering
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

            # Powerup rendering
            for powerup in active_powerups:
                powerup.draw(window)
                if powerup.check_collected(player) or powerup.check_collected(level):
                    active_powerups.remove(powerup)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            
            # Checks if the powerup has been used for too long and reverts to the original value PLAYER
            if player.faster_collected != 0 and pygame.time.get_ticks() - player.faster_collected > POWERUP_EFFECT_DURATION:
                player.max_speed = player.speed_base
            if player.highjump_collected != 0 and pygame.time.get_ticks() - player.highjump_collected > POWERUP_EFFECT_DURATION:
                player.jump_force = player.jump_base
            if player.longerboost_collected != 0 and pygame.time.get_ticks() - player.longerboost_collected > POWERUP_EFFECT_DURATION:
                player.boost_time = player.boost_base

            # Checks if the powerup has been used for too long and reverts to the original value LEVEL
            if level.faster_collected != 0 and pygame.time.get_ticks() - level.faster_collected > POWERUP_EFFECT_DURATION:
                level.max_speed = level.speed_base
            if level.highjump_collected != 0 and pygame.time.get_ticks() - level.highjump_collected > POWERUP_EFFECT_DURATION:
                level.jump_force = level.jump_base
            if level.longerboost_collected != 0 and pygame.time.get_ticks() - level.longerboost_collected > POWERUP_EFFECT_DURATION:
                level.boost_time = level.boost_base
                 
            # Keeps the score of each character
            who_scored = ball.goal(field)
            if who_scored == "player":
                 player_score += 1
            if who_scored == "bot":
                 bot_score += 1

            pygame.display.flip()
        else:
            return "menu"
    return "quit"
            

# Switch between menu and game
while True:
    difficulty = show_menu()
    result = run_game(difficulty)
    if result == "quit":
        break

pygame.quit()