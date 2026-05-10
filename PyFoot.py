import pygame
import random
from base_classes import *
from ball_class import *
from constants import *
from wall_class import *
from PyFoot_UI import *
from powerups import *

"""
This file is the main game loop. It's where all the dots finally connect!
Running this file will let you play our game,
Have fun!
"""

pygame.display.set_caption("PyFoot")
clock = pygame.time.Clock()
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
field = Field()
background = pygame.transform.scale(pygame.image.load("media/grafiti_rood.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
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
    pygame.mixer.music.play(-1)

    # Player and ball creation
    player = Player(Vector2(BW + TH, SCREEN_HEIGHT), Vector2(0,0), 70, 210)
    player_score = 0
    ball = Ball(Vector2(SCREEN_WIDTH/2 - 70, SCREEN_HEIGHT/2 - 70), Vector2(0,0), 70)
    
    starting_time = pygame.time.get_ticks()
    active_powerups = []

    # Bot creation
    if difficulty == "Easy":
        level = EasyBot(Vector2(SCREEN_WIDTH - BW - TH - 100, SCREEN_HEIGHT), Vector2(0,0), 70, 210, player, ball)
    elif difficulty == "Medium":
        level = MediumBot(Vector2(SCREEN_WIDTH - BW - TH - 100, SCREEN_HEIGHT), Vector2(0,0), 70, 210, player, ball)
    elif difficulty == "Hard":
        level = HardBot(Vector2(SCREEN_WIDTH - BW - TH - 100, SCREEN_HEIGHT), Vector2(0,0), 70, 210, player, ball, starting_time)
    bot_score = 0

    font = pygame.font.SysFont(None, 60)
    font_big = pygame.font.SysFont(None, 200)

    def show_overlay(text, duration_ms):
        """Freezes the scene and displays centered text for duration_ms milliseconds."""
        start = pygame.time.get_ticks()
        while pygame.time.get_ticks() - start < duration_ms:
            clock.tick(60)
            window.blit(background, (0, 0))
            draw_boundaries(window)
            level.draw(window)
            ball.draw(window)
            player.draw(window)
            surf = font_big.render(text, True, (255, 0, 0))
            window.blit(surf, surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            pygame.display.flip()

    for count in ["3", "2", "1", "GO!"]:
        show_overlay(count, 1000)

    starting_time = pygame.time.get_ticks()
    last_powerup_time = starting_time

    # Game loop
    run = True
    while run:
        if (pygame.time.get_ticks()- starting_time) < GAME_DURATION:
            dt = clock.tick(60) / 1000  # dt is roughly 0.016 at 60fps

            window.blit(background, (0, 0))

            # Score display
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
            level.bounce_triangle(triangles)
            
            # Ball rendering
            ball.draw(window)
            ball.update(dt, field, player, level, triangles)

            # Player rendering
            player.draw(window)    
            player.update(dt, field)
            player._handle_inputs(dt, field)
            player.bounce_triangle(triangles)
            player.collision_player_bot(level)

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
                player.faster_collected = 0
            if player.highjump_collected != 0 and pygame.time.get_ticks() - player.highjump_collected > POWERUP_EFFECT_DURATION:
                player.jump_force = player.jump_base
                player.highjump_collected = 0
            if player.longerboost_collected != 0 and pygame.time.get_ticks() - player.longerboost_collected > POWERUP_EFFECT_DURATION:
                player.boost_time = player.boost_base
                player.longerboost_collected = 0

            # Checks if the powerup has been used for too long and reverts to the original value LEVEL
            if level.faster_collected != 0 and pygame.time.get_ticks() - level.faster_collected > POWERUP_EFFECT_DURATION:
                level.max_speed = level.speed_base
                level.faster_collected = 0
            if level.highjump_collected != 0 and pygame.time.get_ticks() - level.highjump_collected > POWERUP_EFFECT_DURATION:
                level.jump_force = level.jump_base
                level.highjump_collected = 0
            if level.longerboost_collected != 0 and pygame.time.get_ticks() - level.longerboost_collected > POWERUP_EFFECT_DURATION:
                level.boost_time = level.boost_base
                level.longerboost_collected = 0
                 
            # Keeps the score of each character and resets the position
            who_scored = ball.goal(field)
            if who_scored:
                if who_scored == "player":
                    player_score += 1
                else:
                    bot_score += 1
                player.pos = Vector2(BW + TH, SCREEN_HEIGHT)
                player.velocity = Vector2(0, 0)
                level.pos = Vector2(SCREEN_WIDTH - BW - TH - 100, SCREEN_HEIGHT)
                level.velocity = Vector2(0, 0)
                active_powerups.clear()
                show_overlay("GOAL!", 2000)

            pygame.display.flip()
        else:
            pygame.mixer.music.stop()
            return show_end_screen(player_score, bot_score)
    pygame.mixer.music.stop()
    return "quit"
            
pygame.mixer.init()
pygame.mixer.music.load("media/Formula 1 Theme [_QmiNC9d788].mp3")

# Gives the selected difficulty to the game runner
while True:
    difficulty = show_menu()
    if difficulty == "tutorial":
        show_tutorial()
        continue
    result = run_game(difficulty)
    if result == "quit":
        break

pygame.quit()